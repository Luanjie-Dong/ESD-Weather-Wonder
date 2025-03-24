"use client"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { CloudLightning } from "lucide-react"
import { useState , useEffect} from "react";
import axios from "axios";
import { isAuthenticated } from "./lib/auth"
import { login } from "./lib/auth"


export default function LandingPage() {
  const api_name = process.env.NEXT_PUBLIC_API_KEY_NAME
  const api_key = process.env.NEXT_PUBLIC_API_KEY_VALUE
  if (!api_name || !api_key) {
    throw new Error("API key or name is missing");
  }
  
  const [loading , setLoading] = useState(false)
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    country: "",
    state: "",
    city: ""
  });

  const [loginData, setLoginData] = useState({
    email: "",
    password:""
  });

  const handleCreationChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleLoginChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setLoginData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };


  const handleCreation = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault(); 
    setLoading(true);
    console.log(formData)
    try {

      const headers = {
        "Content-Type": "application/json", 
        [api_name]: api_key,               
      }
      console.log(headers)
      const response = await axios.post(
        "http://localhost:8000/user-api/v1/signup",
        formData,
        { headers }
      );

      if (response.status == 201){
        console.log("Success:", response.data);
        alert("Account created successfully!");
        login()
        window.location.href = "/dashboard";
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to create account. Please try again.");
    }
  };

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault(); 

    console.log(loginData)
    login()
    window.location.href = "/dashboard";
    // try {
    //   const response = await axios.post("http://localhost:8000/user-api/v1/signup", formData);
    //   console.log("Success:", response.data);
    //   alert("Account created successfully!");
    // } catch (error) {
    //   console.error("Error:", error);
    //   alert("Failed to create account. Please try again.");
    // }
  };


  return (
    <div className="flex min-h-screen flex-col bg-white">
      <header className="border-b border-gray-200 bg-white">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <CloudLightning className="h-6 w-6 text-brand" />
            <span className="text-xl font-bold text-brand">Weather Wonder</span>
          </div>
          <Button asChild variant="outline">
            <Link href="?tab=login">Sign In</Link>
          </Button>
        </div>
      </header>

      <main className="flex-1 bg-white">
        <div className="container grid items-center gap-6 pb-8 pt-6 md:grid-cols-2 md:py-10">
          <div className="flex flex-col justify-center space-y-4">
            <div className="space-y-2">
              <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">Stay ahead of the weather</h1>
              <p className="text-muted-foreground md:text-xl">
                Get real-time weather updates and emergency alerts for your favorite locations.
              </p>
            </div>

            <div className="flex flex-col gap-2 sm:flex-row">
              <Button size="lg" asChild>
                <Link href="?tab=signup">Get Started</Link>
              </Button>
              <Button variant="outline" size="lg">
                Learn More
              </Button>
            </div>

            <div className="mt-4 grid grid-cols-3 gap-2 text-center">
              <div className="rounded-lg bg-muted p-2">
                <p className="text-2xl font-bold">100+</p>
                <p className="text-xs text-muted-foreground">Countries</p>
              </div>
              <div className="rounded-lg bg-muted p-2">
                <p className="text-2xl font-bold">10K+</p>
                <p className="text-xs text-muted-foreground">Cities</p>
              </div>
              <div className="rounded-lg bg-muted p-2">
                <p className="text-2xl font-bold">24/7</p>
                <p className="text-xs text-muted-foreground">Alerts</p>
              </div>
            </div>
          </div>

          <div className="flex justify-center">
            <Tabs defaultValue="signup" className="w-full max-w-md">
              <TabsList className="grid w-full grid-cols-2 gap-2">
                <TabsTrigger value="signup" className="border border-indigo-600">Sign Up</TabsTrigger>
                <TabsTrigger value="login" className="border border-red-600">Log In</TabsTrigger>
              </TabsList>

              <TabsContent value="signup" className={`relative ${loading ? "blur-sm pointer-events-none" : ""} space-y-4 `}>
                <form onSubmit={handleCreation}>
                <Card>
                  <CardHeader>
                    <CardTitle>Create an account</CardTitle>
                    <CardDescription>Enter your information to create an account</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="name">Name</Label>
                      <Input id="name" name="name" placeholder="John Doe" value={formData.name} onChange={handleCreationChange}/>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="email">Email</Label>
                      <Input id="email" name="email" type="email" placeholder="john@example.com" value={formData.email} onChange={handleCreationChange}/>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="password">Password</Label>
                      <Input id="password" name="password" type="password" value={formData.password} onChange={handleCreationChange}/>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="location">Country</Label>
                      <Input id="country" name="country" placeholder="Country" value={formData.country} onChange={handleCreationChange}/>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="location">State</Label>
                      <Input id="state" name="state" placeholder="State" value={formData.state} onChange={handleCreationChange}/>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="location">City</Label>
                      <Input id="city" name="city" placeholder="City" value={formData.city} onChange={handleCreationChange}/>
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Button className="w-full" type="submit">Create Account</Button>
                  </CardFooter>
                </Card>
                </form>
                {loading && (
                  <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
                    <p className="text-white text-lg font-semibold">Creating Account...</p>
                  </div>
                )}
              </TabsContent>

              <TabsContent value="login" className={`relative ${loading ? "blur-sm pointer-events-none" : ""} space-y-4 `}>
                <form onSubmit={handleLogin}>
                <Card>
                  <CardHeader>
                    <CardTitle>Log in</CardTitle>
                    <CardDescription>Enter your credentials to access your account</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <Label htmlFor="Email">Email</Label>
                      <Input id="state" name="email" placeholder="john@example.com" value={loginData.email} onChange={handleLoginChange}/>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="password">Password</Label>
                      <Input id="password" name="password" type="password" value={loginData.password} onChange={handleLoginChange}/>
                    </div>
                  </CardContent>
                  <CardFooter className="flex flex-col space-y-2">
                  <Button className="w-full" type="submit">Login</Button>
                  </CardFooter>
                </Card>
                </form>
                {loading && (
                  <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
                    <p className="text-white text-lg font-semibold">Logging in..</p>
                  </div>
                )}
              </TabsContent>

            </Tabs>
          </div>
        </div>
      </main>

      <footer className="bg-white py-6 border-t border-gray-200">
        <div className="container text-center text-sm text-gray-500">© 2025 Weather Wonder. All rights reserved.</div>
      </footer>
    </div>
  )
}
