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
import { isAuthenticated } from "../lib/auth"
import { login } from "../lib/auth"
import AuthCheck from "@/components/auth-check"
import Swal from 'sweetalert2';

interface FormData {
  email: string;
  password: string;
  [key: string]: any; 
}

interface LoginData {
  email: string;
  password: string;
}

interface Headers {
  Authorization?: string;
  [key: string]: any; 
}

export default function LoginPage() {
    const DASHBOARD_URL = "/dashboard";
    const api_name = process.env.NEXT_PUBLIC_API_KEY_NAME
    const api_key = process.env.NEXT_PUBLIC_API_KEY_VALUE
    const signup_url = `${process.env.NEXT_PUBLIC_API_GATEWAY_URL}/user-api/v1/signup`
    const login_url = `${process.env.NEXT_PUBLIC_API_GATEWAY_URL}/user-api/v1/signin`
    const add_location_endpoint = `${process.env.NEXT_PUBLIC_API_GATEWAY_URL}/add-user-location-api/v1/add_location`

    if (!api_name || !api_key) {
      throw new Error("API key or name is missing");
    }
  
    const headers = {
      "Content-Type": "application/json", 
      [api_name]: api_key,               
    }
    
    const [invalid,setInvalid] = useState(false)
    const [loading , setLoading] = useState(false)
    const [formData, setFormData] = useState({
      username: "",
      email: "",
      password: "",
      country: "",
      state: "",
      city: "",
      neighbourhood:"",
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
    
      try {
        console.log(formData);
        const response = await axios.post(signup_url, formData as FormData, { headers: headers as Headers });
    
        if (response.status === 201) {
          Swal.fire({
            icon: 'success',
            title: 'Account Created Successfully!',
            text: 'You will now be redirected to the dashboard.',
            confirmButtonText: 'OK',
          }).then(async () => {
            try {
              const userDetail = {
                email: formData['email'],
                password: formData['password'],
              };
              const responseUser = await axios.post(login_url, userDetail, { headers: headers as Headers });
              const userProfile = responseUser.data?.user;
    
              await addLocation(userProfile); 
              await handleUserLogin(userProfile); 
            } catch (loginError) {
              handleError(loginError, 'Failed to log in after account creation. Please try again.');
            }
          });
        }
      } catch (error) {
        handleError(error, 'Failed to create account. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    const constructAddress = (userProfile: any): string => {
      const addressParts = [
        userProfile?.['Country'],
        userProfile?.['State'],
        userProfile?.['City'],
        userProfile?.['Neighbourhood'],
      ].filter(Boolean); 
    
      const address = addressParts.join(", "); 

      return address;
    };
  
    const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      setInvalid(false);
    
      try {
        const responseUser = await axios.post(login_url, loginData as LoginData, { headers: headers as Headers });
    
        if (responseUser.status === 404) {
          setInvalid(true);
        } else {
          const userProfile = responseUser.data?.user;
          if (!userProfile) {
            throw new Error("User profile not found in response.");
          }
    
          await handleUserLogin(userProfile);
        }
      } catch (error) {
        handleError(error, 'Failed to log in. Please try again.');
      }
    };

    const handleUserLogin = async (userProfile: any) => {
      try {
        login(userProfile);
        window.location.href = DASHBOARD_URL;
      } catch (error) {
        console.error("Error during login:", error);
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'Failed to log in. Please try again.',
        });
      }
    };

    const addLocation = async (userProfile: any) => {
      try {
        const address = constructAddress(userProfile);
        const payload = {"address":address,"label":"Home",'user_id':userProfile.user_id}

        const response = await axios.post(add_location_endpoint, payload, { headers: headers as Headers });
    
        if (response.status === 500) {
          throw new Error("Failed to add location due to server error.");
        }
      } catch (error) {
        console.log(error, 'Failed to add location. Please try again after you log in.');
      }
    };

    const handleError = (error: any, defaultMessage: string) => {
      if (axios.isAxiosError(error)) {
        const errorMessage = error.response?.data?.message || defaultMessage;
        console.error("Error:", errorMessage);
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: errorMessage,
        });
      } else {
        console.error("Unknown Error:", error);
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: defaultMessage,
        });
      }
    };
  
  
    return (
      <div className="flex min-h-screen flex-col bg-white">
        <header className="border-b border-gray-200 bg-white">
          <div className="container flex h-16 items-center justify-between">
            <div className="flex items-center gap-2">
              <CloudLightning className="h-6 w-6 text-brand" />
              <span className="text-xl font-bold text-brand">Weather Wonder</span>
            </div>
            {/* <Button asChild variant="outline">
              <Link href="?tab=login">Sign In</Link>
            </Button> */}
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
                  <TabsTrigger value="signup" className="border border-indigo-600 hover:bg-indigo-600 hover:text-white">Sign Up</TabsTrigger>
                  <TabsTrigger value="login" className="border border-red-600 hover:bg-red-600 hover:text-white">Log In</TabsTrigger>
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
                        <Input id="name" name="username" placeholder="John Doe" value={formData.username} onChange={handleCreationChange}/>
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="email">Email</Label>
                        <Input id="email" name="email" type="email" placeholder="john@example.com" value={formData.email} onChange={handleCreationChange}/>
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="password">Password</Label>
                        <Input id="password" name="password" type="password" value={formData.password} onChange={handleCreationChange}/>
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
                        <div className="space-y-2">
                          <Label htmlFor="location">Neighbourhood</Label>
                          <Input id="city" name="neighbourhood" placeholder="Neighbourhood" value={formData.neighbourhood} onChange={handleCreationChange}/>
                        </div>
                      </div>
                      
                    </CardContent>
                    <CardFooter>
                      <Button className="w-full hover:bg-gray-300" type="submit">Create Account</Button>
                    </CardFooter>
                  </Card>
                  </form>
                  {loading && (
                    <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
                      <p className="text-white text-lg font-semibold">Creating Account...</p>
                    </div>
                  )}
                </TabsContent>
  
                <TabsContent value="login" className={`relative ${loading ? "blur-lg pointer-events-none" : ""} space-y-4 `}>
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
                      {invalid && (
                      <div className="text-center py-4">
                        <p className="text-red-900 text-lg font-semibold">WRONG USER EMAIL! Try again :)</p>
                      </div>
                      )}
                    <CardFooter className="flex flex-col space-y-2">
                    <Button className="w-full hover:bg-gray-300" type="submit">Login</Button>
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
  