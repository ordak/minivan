fancizeSpace = function(c) { return c == ' ' ? '□ ' : c; };
crankUpAndDomizeColor = function(baseColor, crankFactor) {
    overflowFactor = crankFactor > 1 ? crankFactor - 1 : 0;
    overflowFactor = crankFactor;
    return "rgb(" + (baseColor[0] * crankFactor + overflowFactor * 40) + 
              "," + (baseColor[1] * crankFactor + overflowFactor * 40) + 
              "," + (baseColor[2] * crankFactor + overflowFactor * 40) + 
              ")";
}
