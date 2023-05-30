import { useState, useEffect } from 'react';
import { createClient } from '@supabase/supabase-js';
import axios from 'axios';


const isDevelopment = false;

var backendUrl = "http://localhost:8000";

if (isDevelopment) {
  backendUrl = "http://localhost:8000"
}
const supabaseUrl = 'https://jkohjbndimwjcyobeuaf.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imprb2hqYm5kaW13amN5b2JldWFmIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODUyNTcxODIsImV4cCI6MjAwMDgzMzE4Mn0.bICKR1hSTyppYMPx8cEgocdY4IaStBlcIJdlQ1Iymg4'
const supabase = createClient(supabaseUrl, supabaseKey)


function GitHubLogin() {
    const [ sessionData, setLoggedIn ] =  useState(null);
    useEffect(() => {
       supabase.auth.onAuthStateChange(
        (event, session) => {
          // Handle session updates
          if (event === 'SIGNED_IN') {
            console.log('signed in')
          }
          if (session !== null) {
            setLoggedIn(session)
          }
          console.log(event, session)
        }
      )
    }, [setLoggedIn])
  
    const signInWithGithub = async () => {
      const { data, error } = await supabase.auth.signInWithOAuth({
        provider: 'github',
        options: {
          scopes: "codespace,repo",
        }
      })
  
      console.log(data);
  
      if (error) {
        console.log('Error signing in with GitHub:', error.message)
      }
    }
  
  
    if (sessionData) {
      return (
        <div>
          <SetGithubUrl accessToken={sessionData.access_token} email={sessionData.user.email} />
          <SignOut />
        </div>
      );
      
  
    } else {
      return (
        <button onClick={signInWithGithub}>
          Sign in with GitHub
        </button>
      )
    }
}

function SetGithubUrl(props) {
    const [ githubRepoUrl, setGithubRepoUrl ] = useState(null);
    const [ triggeredGithubUrl, setTriggeredGithubUrl ] = useState(null);
  
    function createDevEnvironment(githubRepoUrl) {
      axios.post(backendUrl + "/create-dev-environment", {"githubRepoUrl": githubRepoUrl, "githubAccessToken": props.accessToken, "email": props.email }).then((response) => {
        setTriggeredGithubUrl(githubRepoUrl);
      })
    }
  
    var triggeredGithubUrlText = null;
  
    if (triggeredGithubUrl) {
      triggeredGithubUrlText = (
        <p>
          Setting up dev environment for {triggeredGithubUrl}! You'll get an email when this completes.
        </p>
      )
    }
  
  
    return (
      <div>
        <input type="text" placeholder='github repo url' value={githubRepoUrl} onChange={e => setGithubRepoUrl(e.target.value)} />
        <button onClick={() => createDevEnvironment(githubRepoUrl)}>
          Set Github URL
        </button>
        {triggeredGithubUrlText}
      </div>
    )
  }
  
  
  
  function SignOut() {
    const signOut = async () => {
      const { error } = await supabase.auth.signOut()
  
      if (error) {
        console.log('Error signing out:', error.message)
      }
    }
  
    return (
      <p>
        <button onClick={signOut}>
          Sign out
        </button>
      </p>
  
    )
  } 


export default GitHubLogin;