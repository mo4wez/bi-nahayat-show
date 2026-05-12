# services/search_service.py

from peewee import fn
from functools import reduce
from operator import or_
from services.models import Question, Level, Step
from utils.text_normalizer import normalize_text
import re


STOPWORDS = {
    "ما","من","تو","که","از","با","برای","وقتی","داریم","میخوایم","نیست",
    "هست","یک","یه","میگیم","گفتیم","شد","میشه","کرد","کردیم","اما","اگر"
}

def normalize_query(q):
    q = normalize_text(q)
    q = re.sub(r"[^\w\s]", " ", q)
    tokens = q.split()
    tokens = [t for t in tokens if len(t) > 2 and t not in STOPWORDS]
    return tokens


def build_and(conditions):
    return reduce(lambda a, b: a & b, conditions)


def build_or(conditions):
    return reduce(lambda a, b: a | b, conditions)



class SearchService:
    @staticmethod
    def _base_query():
        return (
            Question
            .select(Question, Step, Level)
            .join(Level)
            .join(Step)
        )

    @staticmethod
    def search_optimized(user_query: str, limit=10):
        normalized = normalize_text(user_query)

        # --- Exact Match ---
        exact = (
            SearchService._base_query()
            .where(fn.LOWER(Question.question_text) == normalized.lower())
            .first()
        )
        if exact:
            return [exact]

        # --- Token-based ---
        tokens = normalize_query(user_query)
        if not tokens:
            return []

        base = SearchService._base_query()

        # Phase 1: AND search
        and_conditions = [
            (fn.LOWER(Question.question_text).contains(t.lower())) |
            (fn.LOWER(fn.COALESCE(Question.tags, "")).contains(t.lower())) |
            (fn.LOWER(fn.COALESCE(Question.hint, "")).contains(t.lower()))
            for t in tokens
        ]
        try_and = base.where(build_and(and_conditions))

        if try_and.exists():
            return try_and.limit(limit)

        # Phase 2: OR fallback — **fixed**
        or_conditions = [
            (fn.LOWER(Question.question_text).contains(t.lower())) |
            (fn.LOWER(fn.COALESCE(Question.tags, "")).contains(t.lower())) |
            (fn.LOWER(fn.COALESCE(Question.hint, "")).contains(t.lower()))
            for t in tokens
        ]
        or_query = base.where(build_or(or_conditions))

        return or_query.limit(limit)
