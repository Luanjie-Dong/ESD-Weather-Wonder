"use client"

import type React from "react"
import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { isAuthenticated } from "../app/lib/auth"
import { usePathname } from 'next/navigation';

export default function AuthCheck({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  const [isClient, setIsClient] = useState(false) 
  const pathname = usePathname();

  useEffect(() => {
    setIsClient(true) 
    if (!isAuthenticated()) {
      router.push('/login');
    } else if (pathname === '/' && isAuthenticated()) {
      router.push('/dashboard');
    }
  }, [router, pathname]);

  if (!isClient) {
    return null 
  }

  if (!isAuthenticated()) {
    return null 
  }

  return <>{children}</>
}