import time

time.sleep(2)

last_info = None


total_space = 200


last_change = None 


while True:
    log = open('temp.txt','r+')
    details = log.readlines()
    log.close()
    
    new_info = details[-1]
    if new_info == '0 0\n' and len(details)==1:
        print('over')
        break
    
    else:

        if new_info == last_info:
            
            pass
        
        else:
            last_info = new_info

            dets = last_info.split(' ')

            up = int(dets[0])
            down = int(dets[-1])

            change = up - down

            if change == last_change:
                break
            else:
                last_change = change

                space = 200 + change
                
                ofile = open('guisrs.txt','w')

                ofile.write(str(space))
                ofile.close()


ofile = open('guisrs.txt','w')
ofile.truncate(0)
ofile.write(str(200))
ofile.close()

                            
                