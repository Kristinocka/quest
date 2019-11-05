from collections import defaultdict

from sanic import Sanic
from sanic.response import json
from functools import reduce
from db.opr import create_table, insert_data, get_data_from_table

quest_app = Sanic()
quest_app.static('/', './quest.html')
quest_app.static('/result', './result.html')
quest_app.static('/static', './static')
TABLE_NAME = 'table1'


@quest_app.post('/answers')
async def post_answers(request):
    data = request.json
    print(data)
    for x in data:
        for val in x['v']:
            insert_data(TABLE_NAME, x["q"], val)
    return json('success')


@quest_app.get('/answers')
async def answers(request):
    q = defaultdict(dict)
    for key, val in get_data_from_table(TABLE_NAME):
        q[key][val] = q[key].get(val, 0) + 1
    amount = reduce(lambda prev, x: min(prev, sum([q[x][y] for y in q[x]])), q, 1e6)

    return json({
        'amount': amount,
        'result': [
            {'q': key, 'v': [{'answer': val, 'percentage': round(q[key][val] / amount * 100, 2)}
                             for val in q[key]]}
            for key in q]
    })


@quest_app.listener("before_server_start")
async def init(app, loop):
    create_table(TABLE_NAME)


if __name__ == "__main__":
    quest_app.run(host="0.0.0.0", port=8000)
