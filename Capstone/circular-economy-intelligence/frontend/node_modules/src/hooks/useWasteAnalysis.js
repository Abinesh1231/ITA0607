import { useState } from "react";
import { analyzeWaste } from "../services/api";
export default function useWasteAnalysis(){
  const [data,setData]=useState(null),[loading,setLoading]=useState(false);
  const analyze=async file=>{setLoading(true);try{setData(await analyzeWaste(file));}finally{setLoading(false);}};
  return {data,loading,analyze};
}
