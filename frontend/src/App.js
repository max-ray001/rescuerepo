import './App.css';
import { createClient } from '@supabase/supabase-js';
import { useEffect, useState } from 'react';
import axios from 'axios';



const isDevelopment = true;

var backendUrl = "http://localhost:8000";

if (isDevelopment) {
  backendUrl = "http://localhost:8000"
}
const supabaseUrl = process.env.SUPABASE_URL
const supabaseKey = process.env.SUPABASE_ANON_KEY
const supabase = createClient(supabaseUrl, supabaseKey)

function App() {
  return (
    <div className="App">
        <h1>
          Auto Repo Resurrection
          
        </h1>

        <p>
          Just type in a Github URL, and get a working development environment back!
        </p>
        <Github />
    </div>
  );
}


export function Github() {
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

export default App;
