from scapy.layers.inet import TCP, IP, Ether, ICMP, UDP
from scapy.packet import Raw

dcid_len = 8

def quic_long_heuristic(udp_payload):
    # Check if the UDP payload is a QUIC packet
    # flag byte (1B) + version (4B) + DCID len (1B) + SCID len (1B) = 7B
    if len(udp_payload) <= 7:
        # not a QUIC Long Header Packet
        return False 

    # Header Form Check
    if (udp_payload[0] & 0x80 != 0x80):
        return False

    # Fixed Bit Check
    if (udp_payload[0] & 0x40 != 0x40):
        return False

    # Check QUIC Version
    version = udp_payload[1:5]
    if(int.from_bytes(version, "big") != 0x1):
        print("Version Mismatch", version.hex())

    offset = 5
    # DCID Length Check
    dcid_len = udp_payload[offset]
    offset += 1 + dcid_len

    if len(udp_payload) <= offset:
        return False

    # SCID Length Check
    scid_len = udp_payload[offset]
    offset += 1 + scid_len

    if len(udp_payload) <= offset:
        return False

    return True


def quic_short_heuristic(udp_payload):
    # Check if the UDP payload is a QUIC packet
    # flag byte (1B) + PKN(1/2/4) + payload (1+) = 18B
    if len(udp_payload) < 3:
        return False

    # Header Form Check
    if (udp_payload[0] & 0x80 != 0x00):
        return False
    
    if (udp_payload[0] & 0x40 != 0x40):
        return False

    return True

def extract_quic_dcid_long_pkt(udp_payload):
    offset = 5
    # DCID Length Check
    dcid_len = udp_payload[offset]
    offset += 1

    dcid = udp_payload[offset:offset+dcid_len]
    return dcid    

def extract_quic_dcid_short_pkt(udp_payload, dcid_len):
    if dcid_len == 0:
        return None
    
    if dcid_len > 20:
        raise ValueError("DCID length is too long")

    if dcid_len > len(udp_payload):
        raise ValueError("DCID length is too long")

    offset = 1
    dcid = udp_payload[offset:offset+dcid_len]
    return dcid

def quic_dcid(pkt) -> bytes | None:
    if UDP in pkt:
        udp_payload = pkt[Raw].load
        
        if udp_payload is None:
            return False

        if quic_long_heuristic(udp_payload):
            print("QUIC Long Header Packet")
            return extract_quic_dcid_long_pkt(udp_payload)

        elif quic_short_heuristic(udp_payload):
            print("QUIC Short Header Packet")
            if len(udp_payload) < dcid_len:
                return None
            else:
                return extract_quic_dcid_short_pkt(udp_payload, dcid_len)
        else:
            print("## Not QUIC Packet ##")
            return None
    else:
        print("## Not UDP Packet ##")
        return None