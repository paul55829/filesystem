import sys
import struct
import math
import stat


BLOCK_SIZE = 1024

def get_data(data, idx, datatype, length):
    return (struct.unpack(datatype, data[idx : idx + length]))[0]


def parse_superblock(sbdata):
    
    sbdict = {}

    idx = 0
    sbdict["n_inodes"] = get_data(sbdata, idx, "<H", 2)
    idx += 2
    sbdict["no_zones"] = get_data(sbdata, idx, "<H", 2)
    idx += 2
    sbdict["imap_blocks"] = get_data(sbdata, idx, "<H", 2)
    idx += 2
    sbdict["zmap_blocks"] = get_data(sbdata, idx, "<H", 2)
    idx += 2
    sbdict["first_data_zone"] = get_data(sbdata, idx, "<H", 2)
    idx += 2
    sbdict["log_zone_size"] = get_data(sbdata, idx, "<H", 2)
    idx += 2
    sbdict["max_file_size"] = get_data(sbdata, idx, "<L", 4)
    idx += 4
    sbdict["minix_magic"] = get_data(sbdata, idx, "<H", 2)
    idx += 2
    sbdict["log_zone_size"] = get_data(sbdata, idx, "<H", 2)
    idx += 2
    sbdict["mount_state"] = get_data(sbdata, idx, "<H", 2)
    idx += 2

    return sbdict

def parse_inode(indata):
    inode_dict = {}

    idx = 0
    inode_dict["MODE"] = get_data(indata, idx, "<H", 2)
    idx += 2
    inode_dict["UID"] = get_data(indata, idx, "<H", 2)
    idx += 2
    inode_dict["SIZE"] = get_data(indata, idx, "<L", 4)
    idx += 4
    inode_dict["TIME"] = get_data(indata, idx, "<L", 4)
    idx += 4
    inode_dict["GID"] = get_data(indata, idx, "<B", 1)
    idx += 1
    inode_dict["LINKS"] = get_data(indata, idx, "<B", 1)
    idx += 1
    inode_dict["zone0"] = get_data(indata, idx, "<H", 2)
    idx += 2
    inode_dict["zone1"] = get_data(indata, idx, "<H", 2)
    idx += 2
    inode_dict["zone2"] = get_data(indata, idx, "<H", 2)
    idx += 2
    inode_dict["zone3"] = get_data(indata, idx, "<H", 2)
    idx += 2
    inode_dict["zone4"] = get_data(indata, idx, "<H", 2)
    idx += 2
    inode_dict["zone5"] = get_data(indata, idx, "<H", 2)
    idx += 2
    inode_dict["zone6"] = get_data(indata, idx, "<H", 2)
    idx += 2
    inode_dict["zone7"] = get_data(indata, idx, "<H", 2)
    idx += 2
    inode_dict["zone8"] = get_data(indata, idx, "<H", 2)
    idx += 2

    return inode_dict

def parse_directory(dir_data):
    dir_dict = {}

    idx = 0
    dir_dict["number"] = get_data(dir_data, idx, "<H", 2)
    idx += 2
    dir_dict["name"] = get_data(dir_data, idx, "<14s", 14)
    idx += 14

    return dir_dict

# def get_used_inodes(inodes_map):
#     used_inodes = []
#     idx = 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: mfstool.py image command params")
        sys.exit(0)

    diskimg = sys.argv[1]
    cmd = sys.argv[2]

    with open(diskimg, "rb") as f:

        # Skip boot block.
        f.seek(BLOCK_SIZE, 1)

        # Read super block.
        sbdata = f.read(BLOCK_SIZE)

        # Parse super block intfor i inparse_inode sbdict dictionary.
        sbdict = parse_superblock(sbdata)

        # Read inode map
        size_inode_map = sbdict["imap_blocks"] * BLOCK_SIZE
        inode_map = f.read(size_inode_map)
        # get_used_inodes(inode_map)

        # Skip zone_map
        size_zone_map = sbdict["zmap_blocks"] * BLOCK_SIZE
        f.seek(size_zone_map, 1)

        i = 0
        while i < sbdict["n_inodes"]:
            inode = f.read(32)
            parsed_inode = parse_inode(inode)

            if stat.S_ISDIR(parsed_inode["MODE"]):
                # Inode contains info about directory, go to the directory
                location = parsed_inode["zone0"]
                f.seek(BLOCK_SIZE * location)
                print(parsed_inode)
                # Read and print directory names
                # while
                dir = f.read(16)
                parsed_dir = parse_directory(dir)
                print(parsed_dir["name"].decode("ASCII"))

            if stat.S_ISREG(parsed_inode["MODE"]):
                # Inode contains info about file, go to the file
                location = parsed_inode["zone0"]
                f.seek(BLOCK_SIZE * location)

            i += 1



        
        # f.seek(15 * BLOCK_SIZE, 0)

        # print(inodes[0])
        # print(inodes[0]["zone0"])
        # block_location = inodes[0]["zone0"] * BLOCK_SIZE
        # print(block_location)
        # data_block = f.seek(block_location, 0)

        # blocks = inodes[0]["size"] / 16
        # for i in range(blocks):
        #     dir = data_block.read(16)
        #     parsed_dir = parse_directory(dir)
        #     print(parse_directory["name"])
