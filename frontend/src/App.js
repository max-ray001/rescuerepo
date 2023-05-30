import './App.css';
import { createClient } from '@supabase/supabase-js';
import Title from './components/Title';
import Button from './components/PrimaryButton';



const isDevelopment = false;

var backendUrl = "http://localhost:8000";

if (isDevelopment) {
  backendUrl = "http://localhost:8000"
}
const supabaseUrl = 'https://jkohjbndimwjcyobeuaf.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imprb2hqYm5kaW13amN5b2JldWFmIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODUyNTcxODIsImV4cCI6MjAwMDgzMzE4Mn0.bICKR1hSTyppYMPx8cEgocdY4IaStBlcIJdlQ1Iymg4'
const supabase = createClient(supabaseUrl, supabaseKey)


function App() {

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

  return (
    <div className="grid grid-cols-2 p-4 h-screen">
      <div className="flex flex-col justify-center">
        <Title title="reposurrection." subtitle="breathe a second life into your dead repos." className="px-12" />
      </div>
      <div className="flex flex-col h-full w-full justify-center items-center">

        {/* Note: the onClick functionality is the same as the previous GitHub button. */}
        <Button text="sign in with GitHub" onClick={signInWithGithub} className="w-1/2 bg-gray-300 hover:bg-blue-700 text-black text-2xl font-medium py-7 px-6 rounded rounded-xl mx-12" />
      </div>
    </div>
  );
}


export default App;
