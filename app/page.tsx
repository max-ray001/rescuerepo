"use client";
import GithubComponent from "@/components/github/main";

export default function Home() {
  return (
    <div className="px-96 py-40 flex flex-col space-y-24">
      <div className="flex-row space-y-16 text-center">
        <h1 className="text-4xl font-extrabold text-white items-center justify-center text-transparent bg-clip-text bg-gradient-to-r from-zinc-50 to-slate-300">
          RescueRepo
        </h1>
        <h5 className="text-l text-white items-center justify-center ">
          Bioinformatics is littered with Abandonware.
          <br />
          Stop spending precious time setting up dev environments or rebuilding existing tools.
          <br />
          Just type in a Github URL, and get a working development environment back!
        </h5>
      </div>
      <GithubComponent />
      <div className="flex-row space-y-16 text-center">
        <h5 className="text-l text-white items-center justify-center ">
          Want to contribute? <a href="https://github.com/matthew-mcateer/rescuerepo" className="text-l text-indigo-400 ">Check out our source code</a>!
        </h5>
      </div>
    </div>
  );
}