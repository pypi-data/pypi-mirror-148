import sys
import os


sys.path.insert(1, os.path.join(sys.path[0], "../../.."))

from opteryx.engine.planner.temporal import extract_temporal_filters

from opteryx.storage.cache.memory_cache import InMemoryCache
from opteryx.storage.cache.memcached_cache import MemcachedCache

cache = InMemoryCache(size=100)
# cache = MemcachedCache(server="127.0.0.1:11211")

def test(SQL):

    from mabel.utils import timer
    from opteryx.utils.display import ascii_table
    import opteryx
    from opteryx.storage.adapters import DiskStorage

    conn = opteryx.connect(reader=DiskStorage(), cache=cache, partition_scheme=None)
    cur = conn.cursor()

    with timer.Timer():
        # do this to go over the records
        cur.execute(SQL)
        # cur._results = [pyarrow.concat_tables(cur._results)]
        # print("METADATA:", get_metadata(cur._results))

        # print(pyarrow.concat_tables(cur._results))

        print(ascii_table(cur.fetchmany(size=10), limit=10))
        [a for a in cur.fetchmany(1000)]
        print(json.dumps(cur.stats, indent=2))


if __name__ == "__main__":

    import json
    import sqloxide

    # SQL = "SELECT count(*) from `tests.data.zoned` where followers < 10 group by followers"
    # SQL = "SELECT username, count(*) from `tests.data.tweets` group by username"
    SQL = "SELECT COUNT(user_verified) FROM tests.data.set as ds"

    # SQL = """
    # SELECT DISTINCT user_verified, MIN(followers), MAX(followers), COUNT(*)
    #  FROM tests.data.huge
    # GROUP BY user_verified
    # """

    # SQL = "SELECT username from `tests.data.tweets`"

    SQL = "SELECT * FROM $satellites"
    SQL = "SELECT COUNT(*) FROM $satellites"
    SQL = "SELECT MAX(planetId), MIN(planetId), SUM(gm), count(*) FROM $satellites group by planetId"
    SQL = "SELECT upper(name), length(name) FROM $satellites WHERE magnitude = 5.29"
    SQL = "SELECT planetId, Count(*) FROM $satellites group by planetId having count(*) > 5"
    SQL = "SELECT * FROM $satellites order by magnitude, name"
    SQL = "SELECT AVG(gm), MIN(gm), MAX(gm), FIRST(gm), COUNT(*) FROM $satellites GROUP BY planetId"
    SQL = "SELECT COUNT(name) FROM $satellites;"

    SQL = "SELECT name as what_it_known_as FROM $satellites"
    SQL = "SELECT name, id, planetId FROM $satellites"
    SQL = "SELECT COUNT(*), planetId FROM $satellites GROUP BY planetId"
    SQL = "SELECT ROUND(magnitude) FROM $satellites group by ROUND(magnitude)"
    SQL = "SELECT COUNT(*) FROM $satellites"
    SQL = "SELECT * FROM $satellites WHERE (id = 6 OR id = 7 OR id = 8) OR name = 'Europa'"
    SQL = (
        "SELECT BOOLEAN(planetId) FROM $satellites GROUP BY planetId, BOOLEAN(planetId)"
    )
    SQL = "SELECT planetId as pid, round(magnitude) as minmag FROM $satellites"
    SQL = "SELECT RANDOM() FROM $planets"
    SQL = "SELECT RANDOM() FROM $planets"
    SQL = "SELECT TIME()"
    SQL = "SELECT LOWER('NAME')"
    SQL = "SELECT HASH('NAME')"
    SQL = "SELECT * FROM (VALUES (1,2),(3,4),(340,455)) AS t(a,b)"
    # SQL = "SELECT id - 1, name, mass FROM $planets"
    SQL = "SELECT * FROM tests.data.partitioned WHERE $DATE IN ($$PREVIOUS_MONTH)"
    SQL = """
SELECT * FROM (VALUES 
(7369, 'SMITH', 'CLERK', 7902, '02-MAR-1970', 8000, NULL, 20),
(7499, 'ALLEN', 'SALESMAN', 7698, '20-MAR-1971', 1600, 3000, 30),
(7521, 'WARD', 'SALESMAN', 7698, '07-FEB-1983', 1250, 5000, 30),
(7566, 'JONES', 'MANAGER', 7839, '02-JUN-1961', 2975, 50000, 20),
(7654, 'MARTIN', 'SALESMAN', 7698, '28-FEB-1971', 1250, 14000, 30),
(7698, 'BLAKE', 'MANAGER', 7839, '01-JAN-1988', 2850, 12000, 30),
(7782, 'CLARK', 'MANAGER', 7839, '09-APR-1971', 2450, 13000, 10),
(7788, 'SCOTT', 'ANALYST', 7566, '09-DEC-1982', 3000, 1200, 20),
(7839, 'KING', 'PRESIDENT', NULL, '17-JUL-1971', 5000, 1456, 10),
(7844, 'TURNER', 'SALESMAN', 7698, '08-AUG-1971', 1500, 0, 30),
(7876, 'ADAMS', 'CLERK', 7788, '12-MAR-1973', 1100, 0, 20),
(7900, 'JAMES', 'CLERK', 7698, '03-NOV-1971', 950, 0, 30),
(7902, 'FORD', 'ANALYST', 7566, '04-MAR-1961', 3000, 0, 20),
(7934, 'MILLER', 'CLERK', 7782, '21-JAN-1972', 1300, 0, 10))
AS employees (EMPNO, ENAME, JOB, MGR, HIREDATE, SAL, COMM, DEPTNO);
    """
    SQL = """
    SELECT * FROM tests.data.dated
  FOR DATES BETWEEN '2022-02-03' AND '2022-02-03';
      """
    SQL = """
    SELECT *
      FROM $astronaut, UNNEST(Missions) AS Mission
     WHERE Mission = 'Apollo 8'
    """
    SQL = """
    SELECT Birth_Place['town']
      FROM $astronauts
        """
    SQL = "SELECT Birth_Place['town'] FROM $astronauts WHERE Birth_Place['town'] = 'Warsaw'"
    SQL = (
        "SELECT BOOLEAN(planetId) FROM $satellites GROUP BY planetId, BOOLEAN(planetId)"
    )

    SQL = """
    SELECT name FROM $planets WHERE id IN (SELECT * FROM UNNEST((1,2,3)) as id)
    """
    SQL = "SELECT sum(1) FROM $planets;"
    SQL = "SELECT * FROM table_1 FOR SYSTEM_TIME AS OF '2022-02-02'"
    SQL = "SELECT count(*) as c FROM tests.data.dated as d"
    SQL = "SELECT COUNT(*) FROM $astronauts WHERE $astronauts.a = $astronauts.b"
    SQL = "SELECT * FROM $satellites CROSS JOIN $astronauts"
    # SQL = "SELECT * FROM $satellites, $planets USING(id) WHERE id = 1"
    #    SQL = "SELECT * FROM $satellites JOIN $planets ON $satellites.id = $planets.id"
    # SQL = "SELECT s.planetId AS pid FROM $satellites AS s GROUP BY planetId"
    # SQL = "SELECT * FROM $astronauts CROSS JOIN UNNEST(Missions) AS Mission WHERE Mission = 'Apollo 11'"
    SQL = "SELECT * FROM $satellites AS s WHERE $satellites.id = 5 OR s.name = 'Europa'"
    SQL = "SELECT * FROM $planets FOR '2022-03-03' INNER JOIN $satellites ON $planets.id = $satellites.planetId"
    SQL = "SELECT * FROM tests.data.jsonl JOIN tests.data.tweets USING (user_verified)"
    SQL = "SELECT * FROM $astronauts CROSS JOIN UNNEST(Missions) AS Mission WHERE Mission = 'Apollo 11'"
    SQL = "show columns from $satellites LIKE '%id'"
    SQL = "show columns from $satellites LIKE '%id' WHERE column_name = 'id'"
    SQL = " SELECT DISTINCT planetId FROM $satellites LEFT OUTER JOIN $planets ON $satellites.planetId = $planets.id"
    #    SQL = "SELECT distinct planetId FROM $planets left JOIN $satellites ON $planets.id = $satellites.planetId"
    SQL = "SELECT name as nom from $planets"
    SQL = "SELECT a,b,round(a) FROM (VALUES (1,2),(3,4),(340,455)) AS t(a,b) limit 0"
    SQL = "SELECT * FROM $satellites PIVOT( COUNT(planetId) FOR planetId IN (1,2,3,4) )"
    SQL = "SELECT * FROM $satellites LEFT JOIN $planets ON $satellites.planetId = $planets.id WHERE $satellites.name = NONE"

    SQL = "SELECT * FROM $astronauts CROSS JOIN UNNEST(Alma_Mater)"
    SQL = "SELECT Mission FROM $astronauts CROSS JOIN UNNEST(Missions) as Mission WHERE Mission = 'Apollo 11'"
    SQL = "SELECT * FROM $satellites WHERE size = 1"
    #    SQL = "SELECT Missions FROM $astronauts WHERE LIST_CONTAINS(Missions, 'Apollo 8')"
    #SQL = "EXPLAIN SELECT * FROM $satellites LEFT JOIN $planets ON $satellites.planetId = $planets.id WHERE planetId = NONE"
    #SQL = "SELECT * FROM $satellites WHERE name = 'Calypso'"
    SQL = "SELECT * FROM ( SELECT COUNT(*) FROM $planets )"
    SQL = "SELECT * FROM tests.data.dated FOR DATES BETWEEN '2020-02-01' AND '2020-02-28'"
    SQL = "SELECT Name, COUNT(*) AS N FROM $astronauts"
    SQL = "SELECT count(*), VARCHAR(Year) FROM $astronauts GROUP BY VARCHAR(Year)"
    SQL = "SELECT COUNT(*), Birth_Place['town'] FROM $astronauts GROUP BY Birth_Place['town']"
    SQL = "SELECT Birth_Place['town'] AS TOWN FROM $astronauts WHERE Birth_Place['town'] = 'Warsaw'"
    SQL = "SELECT name, id, planetId FROM $satellites"
    SQL = "SELECT CAST(Year AS VARCHAR) FROM $astronauts GROUP BY CAST(Year AS VARCHAR)"
    SQL = "SELECT Name as N, COUNT(*) FROM $astronauts GROUP BY N"
    SQL = "SELECT * FROM $astronauts WHERE VARCHAR(Group) = '10'"

    _, _, SQL = extract_temporal_filters(SQL)
    ast = sqloxide.parse_sql(SQL, dialect="mysql")
    print(json.dumps(ast, indent=2))

    print()

    import cProfile

    with cProfile.Profile(subcalls=False) as pr:
        test(SQL)
