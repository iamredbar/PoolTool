from bitshares import BitShares
import yaml

if __name__ == '__main__':
    base_id = '1.19.'
    count = 0
    invalid_running_count = 0
    end = False
    valid_pools = {'valid_assets': []}
    bs = BitShares()
    while end is not True:
        pool_id = base_id + str(count)
        pool_obj = bs.rpc.get_object(pool_id)
        if pool_obj != None:
            invalid_running_count = 0
            valid_pools['valid_assets'].append(pool_id)
        else:
            invalid_running_count += 1
        
        if invalid_running_count > 4:
            end = True
        
        count += 1

    with open('settings.yml', 'w') as yml:
        yaml.dump(valid_pools, yml)