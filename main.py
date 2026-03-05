import sys


START_COINS = 1_000_000


def all_cities_complete(country_id: int, country_cities, coins, c: int) -> bool:
    """Чи є у кожному місті нашої країни хоча б по одній монеті з кожної іншої країни?"""
    for city_idx in country_cities[country_id]:
        row = coins[city_idx]
        for k in range(c):
            if row[k] == 0:
                return False
    return True


def solve_case(countries):
    """
    countries: list of tuples (name, xl, yl, xh, yh)
    Повертає список (name, days) відсортований за правилом задачі.
    """
    c = len(countries)

    # 1) Побудова міст і належності до країни
    coord_to_city = {}
    city_to_country = []
    country_cities = [[] for _ in range(c)]

    for cid, (name, xl, yl, xh, yh) in enumerate(countries):
        for x in range(xl, xh + 1):
            for y in range(yl, yh + 1):
                if (x, y) in coord_to_city:
                    # За умовою задачі країни не повинні перекриватися.
                    # Якщо все ж перекрились, це вхідна помилка — але програма не падає.
                    continue
                idx = len(city_to_country)
                coord_to_city[(x, y)] = idx
                city_to_country.append(cid)
                country_cities[cid].append(idx)

    n_cities = len(city_to_country)

    # 2) Сусіди
    neighbors = [[] for _ in range(n_cities)]
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for (x, y), i in coord_to_city.items():
        for dx, dy in dirs:
            j = coord_to_city.get((x + dx, y + dy))
            if j is not None:
                neighbors[i].append(j)

    # 3) Монети: coins[city][country]
    coins = [[0] * c for _ in range(n_cities)]
    for city_idx, cid in enumerate(city_to_country):
        coins[city_idx][cid] = START_COINS

    finished_day = [-1] * c

    # Перевірка на день 0
    for cid in range(c):
        if all_cities_complete(cid, country_cities, coins, c):
            finished_day[cid] = 0

    day = 0
    remaining = sum(1 for d in finished_day if d == -1)

    # 4) Симуляція по днях
    while remaining > 0:
        delta = [[0] * c for _ in range(n_cities)]

        # Відправлення "репрезентативної частини" сусідам (обчислено на початку дня)
        for i in range(n_cities):
            deg = len(neighbors[i])
            if deg == 0:
                continue

            row = coins[i]
            for k in range(c):
                give = row[k] // 1000
                if give:
                    out = give * deg
                    delta[i][k] -= out
                    for j in neighbors[i]:
                        delta[j][k] += give

        # Застосування змін (одночасне оновлення)
        for i in range(n_cities):
            di = delta[i]
            ri = coins[i]
            for k in range(c):
                ri[k] += di[k]

        day += 1

        # Перевірка завершення для ще не завершених країн
        for cid in range(c):
            if finished_day[cid] != -1:
                continue
            if all_cities_complete(cid, country_cities, coins, c):
                finished_day[cid] = day
                remaining -= 1

    # 5) Формування відсортованого результату
    result = []
    for cid, (name, *_rest) in enumerate(countries):
        result.append((name, finished_day[cid]))

    result.sort(key=lambda x: (x[1], x[0]))
    return result


def main():
    lines = [line.rstrip("\n") for line in sys.stdin]
    i = 0
    case_no = 1

    out = []
    while i < len(lines):
        # пропуск порожніх рядків
        while i < len(lines) and lines[i].strip() == "":
            i += 1
        if i >= len(lines):
            break

        c_str = lines[i].strip()
        i += 1
        if not c_str:
            continue
        c = int(c_str)
        if c == 0:
            break

        countries = []
        for _ in range(c):
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            parts = lines[i].split()
            i += 1
            name = parts[0]
            xl, yl, xh, yh = map(int, parts[1:5])
            countries.append((name, xl, yl, xh, yh))

        res = solve_case(countries)

        out.append(f"Case Number {case_no}")
        for name, days in res:
            out.append(f"{name} {days}")
        out.append("")  # порожній рядок після кейсу

        case_no += 1

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":

    main()