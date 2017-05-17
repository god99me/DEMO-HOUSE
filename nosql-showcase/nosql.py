""" NoSQL written in Python"""

import socket

HOST = 'localhost'
PORT = 50505
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
STATS = {
    'PUT': {'success': 0, 'error': 0},
    'GET': {'success': 0, 'error': 0},
    'GETLIST': {'success': 0, 'error': 0},
    'PUTLIST': {'success': 0, 'error': 0},
    'INCREMENT': {'success': 0, 'error': 0},
    'APPEND': {'success': 0, 'error': 0},
    'DELETE': {'success': 0, 'error': 0},
    'STATS': {'success': 0, 'error': 0},
}

# actual database
DATA = {}


def parse_message(msg):
    """Return a tuple containing command, key and the value after type casting"""
    command, key, value, value_type = msg.strip().split(';')
    if value_type:
        if value_type == 'LIST':
            value = value.split(',')
        elif value_type == 'INT':
            value = int(value)
        else:
            value = str(value)
    else:
        value = None
    return command, key, value


def update_stats(command, success):
    """Update the STATS dict with info if executing *command* was a *success*"""
    if success:
        STATS[command]['success'] += 1
    else:
        STATS[command]['error'] += 1


def handle_put(key, value):
    DATA[key] = value
    return True, 'Set [{}] = [{}]'.format(key, value)


def handle_get(key):
    if key not in DATA:
        return False, 'Error: key [{}] not found'.format(key)
    else:
        return True, DATA[key]


def handle_putlist(key, value):
    return handle_put(key, value)


def handle_getlist(key):
    result = exists, value = handle_get(key)
    if not exists:
        return result
    elif not isinstance(value, list):
        return False, 'ERROR: key [[]] contains non-list value [[]]'.format(key, value)
    else:
        return result


def handle_increment(key):
    return_value = exists, value = handle_get(key)
    if not exists:
        return return_value
    elif not isinstance(value, int):
        return (False, 'ERROR: Key [{}] contains non-list value ([{}])'.format(
            key, value))
    else:
        DATA[key] = value + 1
        return True, 'Key [{}] incremented'.format(key, value)


def handle_append(key, value):
    result = exists, list_value = handle_get(key)
    if not exists:
        return result
    elif not isinstance(list_value, list):
        return (False, 'ERROR: Key [{}] contains non-list value ([{}])'.format(
            key, value))
    else:
        DATA[key].append(value)
        return True, 'Key [{}] had value [{}] appended'.format(key, value)


def handle_delete(key):
    if key not in DATA:
        return False, 'ERROR: key [{}] not found and cannot be deleted'.format(key)
    else:
        del DATA[key]
        return True, 'key [{}] has been deleted'.format(key)


def handle_stats():
    return True, str(STATS)

# look-up table connect command to handler
COMMAND_HANDERS = {
    'PUT': handle_put,
    'GET': handle_get,
    'GETLIST': handle_getlist,
    'PUTLIST': handle_putlist,
    'INCREMENT': handle_increment,
    'APPEND': handle_append,
    'DELETE': handle_delete,
    'STATS': handle_stats,
}


def main():
    """ Entry point"""
    SOCKET.bind((HOST, PORT))
    SOCKET.listen(1)

    print('Server start at: %s:%s' % (HOST, PORT))
    print('wait for connection...')

    while True:
        conn, addr = SOCKET.accept()
        print('Connected from [{}]'.format(addr))

        while True:
            data = conn.recv(1024).decode()
            command, key, value = parse_message(data)
            if command == 'STATS':
                response = handle_stats()
            elif command in ('GET', 'GETLIST', 'INCREMENT', 'DELETE'):
                response = COMMAND_HANDERS[command](key)
            elif command in ('PUT', 'PUTLIST', 'APPEND',):
                response = COMMAND_HANDERS[command](key, value)
            else:
                response = (False, 'Unknown command type {}'.format(command))
            update_stats(command, response[0])

            conn.sendall('{};{}'.format(response[0], response[1]).encode())

        conn.close()

if __name__ == '__main__':
    main()

