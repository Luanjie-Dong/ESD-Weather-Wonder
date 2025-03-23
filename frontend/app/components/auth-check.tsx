"use client"

import type React from "react"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { isAuthenticated } from "../lib/auth"

export default function AuthCheck({ children }: { children: React.ReactNode }) {
  const router = useRouter()

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push("/")
    }
  }, [router])

  if (!isAuthenticated()) {
    return null // Or a loading spinner
  }

  return <>{children}</>
}
