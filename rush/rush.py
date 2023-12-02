import redis, json, os
from settings import redis_db_click

# redis_db_click = {'host':'127.0.0.1','port':6379,'password':'Handidata123.','db':3}

click_rush_pool = redis.ConnectionPool(host=redis_db_click.get('host'), port=redis_db_click.get('port'),
                                       db=redis_db_click.get('db'),
                                       decode_responses=True, password=redis_db_click.get('password'))
click_redis = redis.StrictRedis(connection_pool=click_rush_pool)


#
def Import_rush(path):
    with open(path, 'r') as f:
        content = json.loads(f.read())
        for i in content.keys():
            click_redis.set(i, content.get(i))
    print(f'{path} 导入完成！')


def export_rush(name='icon'):
    keys = click_redis.keys()
    with open(f'{name}.json', 'w', encoding='utf8') as f:
        item = {}
        for index, i in enumerate(keys):
            print(index)
            if name in i:
                try:
                    item[i] = click_redis.rpoplpush(i, i)
                except:
                    item[i] = click_redis.get(i)
        f.write(json.dumps(item))


if __name__ == '__main__':
    # export_rush('icon')
    # Import_rush('space.json')
    Import_rush('word.json')
