def eor(x, y=list):
  """
> Example: if eor(num, [1,2,3,4,5]):
             <Do something>
           else:
             <Do something>
>>eor function works like if x == y or x == z: except without the or's and instead a list.
>>noOr is a more advanced version of eor
  """
  num = 0
  
  for object in y:
    test = y[num]
    if test == x:
      return [True, test]
      break
    else:
      num += 1
      if num == len(y):
        return False
        
        break
