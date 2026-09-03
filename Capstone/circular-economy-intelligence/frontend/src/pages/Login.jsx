import { useState } from "react";
import { login } from "../services/api";
export default function Login({onLogin}) {
  const [email,setEmail]=useState(""),[password,setPassword]=useState("");
  async function submit(e){e.preventDefault(); const data=await login(email,password); localStorage.setItem("token",data.access_token); onLogin(data); }
  return <section><h1>Login</h1><form className="card form" onSubmit={submit}><input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)}/><input type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)}/><button className="primary">Login</button></form></section>;
}
