"use client";

import { createClient, Session } from "@supabase/supabase-js";
import { SetStateAction, useEffect, useState } from "react";
import axios from "axios";
import {
  Command,
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
  CommandShortcut,
} from "@/components/ui/command";
import { Github } from "lucide-react";


const isDevelopment = false;

let backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL!;
//let githubUsername = process.env.NEXT_PUBLIC_GH_USERNAME!;
if (isDevelopment) {
  backendUrl = "http://localhost:8000";
} 

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
if (!supabaseUrl || !supabaseKey) {
  throw new Error("SUPABASE_URL and/or SUPABASE_ANON_KEY not found in environment variables");
}
const supabase = createClient(supabaseUrl, supabaseKey);


const GithubComponent = () => {
  const [sessionData, setLoggedIn] = useState<Session | null>(null);

  useEffect(() => {
    supabase.auth.onAuthStateChange((event, session) => {
      // Handle session updates
      if (event === "SIGNED_IN") {
        console.log("signed in");
      }
      if (session !== null) {
        setLoggedIn(session);
      }
      console.log(event, session);
    });
  }, [setLoggedIn]);

  const signInWithGithub = async () => {
    const { data, error } = await supabase.auth.signInWithOAuth({
      provider: "github",
      options: {
        scopes: "codespace,repo",
      },
    });

    console.log(data);

    if (error) {
      console.log("Error signing in with GitHub:", error.message);
    }
  };
  if (sessionData) {
    return (
      <div>
        <SetGithubUrl
          accessToken={sessionData.access_token}
          email={sessionData.user.email}
        />
        <br />
        <SignOut />
      </div>
    );
  } else {
    return (
      <button
        className="text-white rounded p-3 mx-auto w-40"
        onClick={signInWithGithub}
      >
        <span className="text-l text-green-400 ">Sign in with GitHub</span>
        
      </button>
    );
  }
};

const SetGithubUrl = (props: { accessToken: any; email: any; }) => {
  const [githubRepoUrl, setGithubRepoUrl] = useState<string | null>(null);
  const [triggeredGithubUrl, setTriggeredGithubUrl] = useState<string | null>(null);
  
  function createDevEnvironment(githubRepoUrl: string) {
    // update the state before the request is made
    setTriggeredGithubUrl(githubRepoUrl);

    // TODO: figure out why the props.accessToken is not serving the purpose of the classic scoped GitHub access tokens
    // TODO: figure out way of obtaining github username from supabase or session data
    axios
      .post(backendUrl + "/api/create-dev-environment", {
        // githubUsername: githubUsername,
        githubRepoUrl: githubRepoUrl,
        githubAccessToken: props.accessToken,
        email: props.email,
      })
      .then((response) => {
        // Handle the response here if needed
        console.log(response);
      })
      .catch((error) => {
        // Handle the error here if needed
        console.error(error);
      
        // If there is an error, clear the message
        setTriggeredGithubUrl(null);
      });
  }

  let triggeredGithubUrlText = null;

  if (triggeredGithubUrl) {
    triggeredGithubUrlText = (
      <p>
        <span className="text-l text-green-400 ">Setting up dev environment for </span>
        <span className="text-l text-green-300 ">{triggeredGithubUrl}</span>
        <span className="text-l text-green-400 ">! You will get an email when this completes.</span>
      </p>
    );
  }

  return (

    <Command className="rounded-lg border shadow-md bg-slate-900 bg-opacity-10 backdrop-blur-md stroke-slate-200">
      <CommandInput
        value={githubRepoUrl || ""}
        onValueChange={setGithubRepoUrl}
        placeholder="Enter a GitHub URL..."
        className="text-white stroke-slate-200"
      />
      <div>
        <button onClick={() => createDevEnvironment(githubRepoUrl)}>
          <span className="text-l text-indigo-400 ">Build Dev Environment for Repo at URL</span>
        </button>
          {triggeredGithubUrlText}
      </div>
      <CommandList>
        <CommandEmpty className="text-white text-center py-10  stroke-slate-200">
          No preexisting results found.
        </CommandEmpty>
        <CommandItem>
          <Github className="mr-2 h-4 w-4 text-white stroke-slate-200" />
          <button onClick={() => githubRepoUrl && createDevEnvironment(githubRepoUrl)} className="text-white">
            {githubRepoUrl}
          </button>
        </CommandItem>
        <CommandGroup heading="Suggestions" className="text-white">
        <CommandItem>
            <Github className="mr-2 h-4 w-4 text-white stroke-slate-200" />
            <span>https://github.com/lucidrains/progen</span>
          </CommandItem>
          <CommandItem>
            <Github className="mr-2 h-4 w-4 text-white stroke-slate-200" />
            <span>https://github.com/lucidrains/alphafold2</span>
          </CommandItem>
          <CommandItem>
            <Github className="mr-2 h-4 w-4 text-white stroke-slate-200" />
            <span>https://github.com/aqlaboratory/openfold</span>
          </CommandItem>
          <CommandItem>
            <Github className="mr-2 h-4 w-4 text-white stroke-slate-200" />
            <span>https://github.com/facebookresearch/esm</span>
          </CommandItem>
          <CommandItem>
            <Github className="mr-2 h-4 w-4 text-white stroke-slate-200" />
            <span>https://github.com/NVIDIA/MegaMolBART</span>
          </CommandItem>
          <CommandItem>
            <Github className="mr-2 h-4 w-4 text-white stroke-slate-200" />
            <span>https://github.com/calvin-zcx/moflow</span>
          </CommandItem>
          <CommandItem>
            <Github className="mr-2 h-4 w-4 text-white stroke-slate-200" />
            <span>https://github.com/gcorso/DiffDock</span>
          </CommandItem>
        </CommandGroup>
      </CommandList>
    </Command>
  );
};

const SignOut = () => {
  const signOut = async () => {
    const { error } = await supabase.auth.signOut();

    if (error) {
      console.log("Error signing out:", error.message);
    }
    // reload the page
    window.location.reload();
  };

  return (
    <p className="text-white">
      <button onClick={signOut}>
        <span className="text-l text-red-400 ">Sign out</span>
      </button>
    </p>
  );
};

export default GithubComponent;
