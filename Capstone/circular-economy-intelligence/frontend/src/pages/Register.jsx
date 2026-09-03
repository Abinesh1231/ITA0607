import { useState } from "react";
import { register } from "../services/api";
export default function Register() {
  const [name,setName]=useState(""),[email,setEmail]=useState(""),[password,setPassword]=useState("");
  async function submit(e){e.preventDefault(); await register(name,email,password); alert("Registration successful. You can now log in.");}
  return <section><h1>Register</h1><form className="card form" onSubmit={submit}><input placeholder="Name" value={name} onChange={e=>setName(e.target.value)}/><input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)}/><input type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)}/><button className="primary">Register</button></form></section>;
}
