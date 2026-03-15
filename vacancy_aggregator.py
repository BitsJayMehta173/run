# vacancy_aggregator.py

from collections import defaultdict


def aggregate_vacancies(rows):

    total = 0
    by_service = defaultdict(int)

    for r in rows:

        v = r["vacancies"]
        s = r["service"]

        total += v

        if s:
            by_service[s] += v

    return {
        "total_vacancies": total,
        "by_service": dict(by_service)
    }