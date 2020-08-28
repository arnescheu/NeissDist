import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from SQLalchemy_declarative import CompDistance, Sub2DistanceUnique

def interrogate_disCrawl(db_input, cutoff, input_queue):
    result_queue = []
    for el in input_queue[1]:
        result_queue.append((el, distance_series(db_input, cutoff, input_queue[0], *el)))
    print(result_queue)

    return result_queue

def distance_series(db_input, cutoff, db_table, min_type, cnt_star, cnt_pideq, dyn_name, poly_eq):
    db_in = create_engine(db_input)
    DB_in_Session = sessionmaker(db_in)
    in_session = DB_in_Session()

    # Query = in_session.query(DCSummary)
    start_time = time.time()

    parametered_query = in_session.query(db_table)
    print("Time (s): ", time.time() - start_time, "\n")

    distance_range = []

    parametered_count = parametered_query.count()
    print('Total count: ', parametered_count)
    print("Time (s): ", time.time() - start_time, "\n")

    print("Query parameters", min_type, cnt_star, cnt_pideq, dyn_name)

    if dyn_name is False:
        pass
    else:
        parametered_query = parametered_query.filter(db_table.dynamic_name == dyn_name)

        parametered_query = parametered_query.filter(db_table.min_type == min_type)

    if poly_eq is False:
        pass
    else:
        parametered_query = parametered_query.filter(db_table.poly_id_eq == poly_eq)

    if cnt_star is False:
        pass
    else:
        parametered_query = parametered_query.filter(db_table.cnt_star == cnt_star)
    if cnt_pideq is False:
        pass
    else:
        parametered_query = parametered_query.filter(db_table.cnt_pideq == cnt_pideq)

    # parametered_query = parametered_query.filter(CompDistance.min_type == 'A') #all
    # parametered_query = parametered_query.filter(CompDistance.min_type == 'I0').filter(CompDistance.cnt_star == 2).filter(CompDistance.cnt_pideq==1) #intra
    # parametered_query = parametered_query.filter(CompDistance.min_type == 'I1E0')#.filter(CompDistance.cnt_pideq == 2) #hetero/inter
    # parametered_query = parametered_query.filter(CompDistance.min_type == 'I1E1') #homo/inter

    parametered_query = parametered_query.order_by(db_table.distance)
    parametered_count = parametered_query.count()
    print('Total count: ', parametered_count)
    print("Time (s): ", time.time() - start_time, "\n")
    distance_range.append(("total", parametered_count))
    for i in range(0, cutoff):
        distance_query = parametered_query.filter(Sub2DistanceUnique.distance < i / 10)
        distance_count = distance_query.count()
        distance_range.append((i, distance_count))
        print(i / 10, distance_count)
    print("Time (s): ", time.time() - start_time, "\n")

    in_session.close()
    return

def write_results(result_queue, outfile):
    results_reordered = [[], []]
    results_reordered[1].append("total")
    for x in range(0, cutoff):
        results_reordered[1].append(x)
    for el in result_queue:
        results_reordered[0].append(el[0])
        results_reordered.append([])
        for x, y in el[1]:
            results_reordered[len(results_reordered) - 1].append(y)
    print(results_reordered)

    with open(outfile, "w+") as outf:
        for i in range(0, cutoff + 1):
            line = ""
            if i == 0:
                line = line + "Cutoff"
                for el in results_reordered[0]:
                    line = line + "|" + str(el)
                print(line)
                outf.write(line + "\n")
                line = ""
            j = 0
            for el in results_reordered:
                if j == 0:
                    pass
                else:
                    line = line + "|" + str(el[i])
                j += 1
            print(line)
            outf.write(line.lstrip("|") + "\n")

if __name__ == "__main__":
    db_input = "sqlite:///disCrawl.db"
    outfile = "outfile.txt"
    cutoff = 501

    #Input_queue to interrogate NeissDist for Figure 2c
    input_queue = (Sub2DistanceUnique,[("N", False, False, "NZ", False), ("NI", False, False, "NZ", False), ("NIE", False, False, "NZ", 0),
                   ("NIE", False, False, "NZ", 1)
        , ("N", False, False, "OH", False), ("NI", False, False, "OH", False), ("NIE", False, False, "OH", 0),
                   ("NIE", False, False, "OH", 1)])

    # input_queue to interrogate NeissDist for Figure 2d
    """
        input_queue = (CompDistance, [("NI", False, False, "NZ", False), ("NI", 1, False, "NZ", False), ("NI", 2, False, "NZ", False), ("NI", 2, 1, "NZ", False), ("NI", 2, 2, "NZ", False),
                   ("NI", 3, False, "NZ", False),
                   ("NIE", False, False,"NZ", 0), ("NIE", 1, False,"NZ", 0), ("NIE", 2, False,"NZ", 0), ("NIE", 2, 1,"NZ", 0), ("NIE", 2, 2,"NZ", 0),
                   ("NIE", 3, False,"NZ", 1), ("NIE", False, False,"NZ", 1), ("NIE", 1, False,"NZ", 1), ("NIE", 2, False,"NZ", 1), ("NIE", 2, 1,"NZ", 1),
                   ("NIE", 2, 2,"NZ", 1),
                   ("NIE", 3, False,"NZ", 1), ("NI", False, False, "OH", False), ("NI", 1, False, "OH", False), ("NI", 2, False, "OH", False), ("NI", 2, 1, "OH", False), ("NI", 2, 2, "OH", False),
                   ("NI", 3, False, "OH", False),
                   ("NIE", False, False,"OH", 0), ("NIE", 1, False,"OH", 0), ("NIE", 2, False,"OH", 0), ("NIE", 2, 1,"OH", 0), ("NIE", 2, 2,"OH", 0),
                   ("NIE", 3, False,"OH", 1), ("NIE", False, False,"OH", 1), ("NIE", 1, False,"OH", 1), ("NIE", 2, False,"OH", 1), ("NIE", 2, 1,"OH", 1),
                   ("NIE", 2, 2,"OH", 1),
                   ("NIE", 3, False,"OH", 1)])

    """

    write_results(interrogate_disCrawl(db_input, cutoff, input_queue),outfile)
