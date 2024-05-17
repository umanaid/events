@app.route('/addtask/<user_id>/<e_id>')
def addtask(user_id,e_id):
    if session.get('user'):
        cursor=mydb.cursor(buffered=True)
        #print(ven_id)
        cursor.execute('select services from events where user_id=(%s)',[user_id])
        data=cursor.fetchall()
    for row in data:
        lst=row[0]
        print(lst)
        l=[]
        for i in lst:
            cursor.execute('select name from vendors WHERE FIND_IN_SET(%s, services) > 0', [i])
            count=cursor.fetchall()
            l.append(count)
            
    print(l)

    cursor.close()
    return render_template('addtask.html',l=l,lst=lst)