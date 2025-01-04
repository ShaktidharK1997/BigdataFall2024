export const getSuccessPhrase = (probability: number, roi: number): string => {
    console.log("ROI = ", roi)
    if (roi <= 100) {
      return "Low Potential: Chance of loss is high";
    } else if (roi > 100 &&  roi <= 200) {
      return "Medium Potential: Chances of breaking even";
    } else if (roi > 200 && roi <= 400) {
      return "Strong Potential: Profitable";
    } else {
        console.log(">500 roi ", roi)
      return "Blockbuster Potential: Exceptionally Profitable";
    }
  };
  
  export const adjustRoi = (roi: number): number => {
    console.log("ROI :", roi)
    return roi;
  };