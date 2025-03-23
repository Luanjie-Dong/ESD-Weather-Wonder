"use client"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { login } from "../lib/auth"
import { useRouter } from "next/navigation"
import type { FormEvent } from "react"

export default function LoginForm() {
  const router = useRouter()

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    login() // Set authenticated state
    router.push("/dashboard")
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="login-email">Email</Label>
        <Input id="login-email" type="email" placeholder="john@example.com" required />
      </div>
      <div className="space-y-2">
        <Label htmlFor="login-password">Password</Label>
        <Input id="login-password" type="password" required />
      </div>
      <Button type="submit" className="w-full">
        Log In
      </Button>
    </form>
  )
}