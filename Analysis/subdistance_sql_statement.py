for i in range(0, 70):
    print('DELETE FROM tempdistance WHERE pdb_id like "%%";')
    print("INSERT INTO tempdistance SELECT *,_rowid_ from distance WHERE static_name = 'C' LIMIT 1000000 OFFSET {};".format(1000000*i))
    print("INSERT INTO subdistance SELECT *, min(distance),'N',_rowid_ from tempdistance WHERE dynamic_name = 'NZ' GROUP BY pdb_id;")
    print("INSERT INTO subdistance SELECT *, min(distance),'NI', _rowid_ from tempdistance WHERE inter is 0 and dynamic_name = 'NZ' GROUP BY pdb_id;")
    print("INSERT INTO subdistance SELECT *, min(distance),'NIE',_rowid_ from tempdistance WHERE inter is 1 and dynamic_name = 'NZ' and not poly_id_eq GROUP BY pdb_id;")
    print("INSERT INTO subdistance SELECT *, min(distance), 'NIE',_rowid_ from tempdistance WHERE inter is 1 and dynamic_name = 'NZ' and poly_id_eq GROUP BY pdb_id;")
    print("INSERT INTO subdistance SELECT *, min(distance),'N',_rowid_ from tempdistance WHERE dynamic_name = 'OH' GROUP BY pdb_id;")
    print("INSERT INTO subdistance SELECT *, min(distance),'NI', _rowid_ from tempdistance WHERE inter is 0 and dynamic_name = 'OH' GROUP BY pdb_id;")
    print("INSERT INTO subdistance SELECT *, min(distance),'NIE',_rowid_ from tempdistance WHERE inter is 1 and dynamic_name = 'OH' and not poly_id_eq GROUP BY pdb_id;")
    print("INSERT INTO subdistance SELECT *, min(distance), 'NIE',_rowid_ from tempdistance WHERE inter is 1 and dynamic_name = 'OH' and poly_id_eq GROUP BY pdb_id;")
