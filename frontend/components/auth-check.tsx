"use client"

import type React from "react"
import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { isAuthenticated } from "../app/lib/auth"

export default function AuthCheck({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  const [isClient, setIsClient] = useState(false) 

  useEffect(() => {
    setIsClient(true) 
    if (!isAuthenticated()) {
      router.push("/")
    }
  }, [router])

  if (!isClient) {
    return null 
  }

  if (!isAuthenticated()) {
    return null 
  }

  return <>{children}</>
}