const seriiDict = (grupe) => {
  console.log('started processing block')
  let currSerie;
  let found;
  let res = []
  for(const grupa of grupe){
    console.log(grupa)
    if(grupa.length == 5){
      currSerie = grupa[-2][0]
    }
    if(grupa.length == 4){
      currSerie = grupa.slice(-1)
    }
    console.log(currSerie)

    found = false;
    for(const serie of res){
      if(serie.serie == currSerie && serie.serie){
        serie.grupe.push(grupa)
        found = true
        break
      }
    }
    
    if(found == false){
      res.push({serie: currSerie, grupe: [grupa]})
    }

  }
  return res
}

let grupe = ['432A', '432B', '432C', '432D', '432E', '432F']
console.log(seriiDict(grupe))