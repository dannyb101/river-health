// Add numerical validation to inputs

 function addPattern(className, regex){ 
    const collection = document.getElementsByClassName(className);
    for (let elem of collection){
      elem.pattern = regex;
    }
  };

// Regex that stops: negative numbers, numbers with commas, numbers of the form .1
// and numbers of the form 1.
no_negs_no_commas_regex = "^[+]?\\d+([.]\\d+)?$"

addPattern('no_negs_no_commas_regex', no_negs_no_commas_regex)

only_pos_ints_regex = "^[1-9]\\d*$"


addPattern('only_pos_ints_regex', only_pos_ints_regex)