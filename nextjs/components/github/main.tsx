"use client";

import { createClient } from "@supabase/supabase-js";
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

const GithubComponent = () => {
  const [sessionData, setLoggedIn] = useState(null);

  const isDevelopment = false;

  let backendUrl = "http://localhost:8000";

  if (isDevelopment) {
    backendUrl = "http://localhost:8000";
  }
  const supabaseUrl = "https://jkohjbndimwjcyobeuaf.supabase.co";
  const supabase = createClient(
    supabaseUrl,
    process.env.NEXT_PUBLIC_SUPABASE_KEY
  );

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
        <SignOut />
      </div>
    );
  } else {
    return (
      <button
        className="text-white rounded p-3 mx-auto w-40"
        onClick={signInWithGithub}
      >
        Sign in with GitHub
      </button>
    );
  }
};

const SetGithubUrl = (props) => {
  const [githubRepoUrl, setGithubRepoUrl] = useState(null);
  const [triggeredGithubUrl, setTriggeredGithubUrl] = useState(null);

  function createDevEnvironment(githubRepoUrl) {
    axios
      .post(backendUrl + "/create-dev-environment", {
        githubRepoUrl: githubRepoUrl,
        githubAccessToken: props.accessToken,
        email: props.email,
      })
      .then((response) => {
        setTriggeredGithubUrl(githubRepoUrl);
      });
  }

  var triggeredGithubUrlText = null;

  if (triggeredGithubUrl) {
    triggeredGithubUrlText = (
      <p>
        Setting up dev environment for {triggeredGithubUrl}! You'll get an email
        when this completes.
      </p>
    );
  }

  return (
    // <div>
    //   <input
    //     type="text"
    //     placeholder="github repo url"
    //     value={githubRepoUrl}
    //     onChange={(e) => setGithubRepoUrl(e.target.value)}
    //   />
    //   <button onClick={() => createDevEnvironment(githubRepoUrl)}>
    //     Set Github URL
    //   </button>
    //   {triggeredGithubUrlText}
    // </div>
    <Command className="rounded-lg border shadow-md bg-slate-900 bg-opacity-10 backdrop-blur-md stroke-slate-200">
      <CommandInput
        value={githubRepoUrl}
        onChange={(e) => setGithubRepoUrl(e.target.value)}
        placeholder="Enter a GitHub URL..."
        className="text-white stroke-slate-200"
      />
      <CommandList>
        <CommandEmpty className="text-white text-center py-10">
          No results found.
        </CommandEmpty>
        <CommandItem>
          <Github className="mr-2 h-4 w-4" />
          <button onClick={() => createDevEnvironment(githubRepoUrl)}>
            GithubRepoUrl
          </button>
        </CommandItem>
        <CommandGroup heading="Suggestions">
          <CommandItem>
            <Github className="mr-2 h-4 w-4" />
            <span>ffmpeg-python</span>
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
  };

  return (
    <p>
      <button onClick={signOut}>Sign out</button>
    </p>
  );
};

export default GithubComponent;
