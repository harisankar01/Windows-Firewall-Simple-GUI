import scapy.all as sc


def capture():
    capture = sc.sniff(filter="tcp", count=50)
    ll = []
    for p in capture:
        a = p.summary()
        ll.append(a)
        # print(a)
    return "\n".join(ll)
