import roslibpy

def main(args=None):
    client = roslibpy.Ros(host="172.17.0.2", port=9090)
    client.run()

    service = roslibpy.Service(client, '/add_two_ints', 'example_interfaces/AddTwoInts')

    request = roslibpy.ServiceRequest({'a': int(args[1]), 'b': int(args[2])})

    result = service.call(request)

    print(f"{request.args['a']} + {request.args['b']} = {result['sum']}")

    client.terminate()

if __name__ == "__main__":
    import sys
    main(args=sys.argv)
