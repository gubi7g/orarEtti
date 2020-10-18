const breakIntoIndividualDivs = (cls) => {
  // ceva gen [1, 3, 4] -> [[1], [3, 4]] doar ca pt grupe
  let res = []
  let tmp = []
  let i = this.groupsArray.indexOf(cls.groups[0])
  for(const grupa of cls.groups){
    if(grupa == this.groupsArray[i]){
      // sunt aceleasi grupe
      tmp.push(this.groupsArray[i])
      i++
    }
    else{
      while(grupa != this.groupsArray[i]){
        i++
      }
      // nu sunt aceleasi grupe. 2 cazuri:
      if(tmp.length){
        res.push(tmp)
        tmp = []
      }
      else{
        //pass
      }
    }
  }

  if(!res.length)
    res.push(tmp)

  console.log(res)

  return res
}

breakIntoIndividualDivs([1, 3, 4])