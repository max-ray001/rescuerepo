#!/usr/bin/env python
import os

DEFAULT_ACCESS_TOKEN = os.environ.get("GH_ACCESS_KEY")
DEFAULT_GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")

# Default few-shot examples

DEFAULT_REPO_URL_FEW_SHOT_EXAMPLE = "https://github.com/kkroening/ffmpeg-python"
DEFAULT_README_FEW_SHOT_EXAMPLE = """# ffmpeg-python: Python bindings for FFmpeg

[![CI][ci-badge]][ci]

[ci-badge]: https://github.com/kkroening/ffmpeg-python/actions/workflows/ci.yml/badge.svg
[ci]: https://github.com/kkroening/ffmpeg-python/actions/workflows/ci.yml

<img src="https://raw.githubusercontent.com/kkroening/ffmpeg-python/master/doc/formula.png" alt="ffmpeg-python logo" width="60%" />

## Overview

There are tons of Python FFmpeg wrappers out there but they seem to lack complex filter support.  `ffmpeg-python` works well for simple as well as complex signal graphs.


## Quickstart

Flip a video horizontally:
```python
import ffmpeg
stream = ffmpeg.input('input.mp4')
stream = ffmpeg.hflip(stream)
stream = ffmpeg.output(stream, 'output.mp4')
ffmpeg.run(stream)
```

Or if you prefer a fluent interface:
```python
import ffmpeg
(
    ffmpeg
    .input('input.mp4')
    .hflip()
    .output('output.mp4')
    .run()
)
```

## [API reference](https://kkroening.github.io/ffmpeg-python/)

## Complex filter graphs
FFmpeg is extremely powerful, but its command-line interface gets really complicated rather quickly - especially when working with signal graphs and doing anything more than trivial.

Take for example a signal graph that looks like this:

![Signal graph](https://raw.githubusercontent.com/kkroening/ffmpeg-python/master/doc/graph1.png)

The corresponding command-line arguments are pretty gnarly:
```bash
ffmpeg -i input.mp4 -i overlay.png -filter_complex "[0]trim=start_frame=10:end_frame=20[v0];\
    [0]trim=start_frame=30:end_frame=40[v1];[v0][v1]concat=n=2[v2];[1]hflip[v3];\
    [v2][v3]overlay=eof_action=repeat[v4];[v4]drawbox=50:50:120:120:red:t=5[v5]"\
    -map [v5] output.mp4
```

Maybe this looks great to you, but if you're not an FFmpeg command-line expert, it probably looks alien.

If you're like me and find Python to be powerful and readable, it's easier with `ffmpeg-python`:
```python
import ffmpeg

in_file = ffmpeg.input('input.mp4')
overlay_file = ffmpeg.input('overlay.png')
(
    ffmpeg
    .concat(
        in_file.trim(start_frame=10, end_frame=20),
        in_file.trim(start_frame=30, end_frame=40),
    )
    .overlay(overlay_file.hflip())
    .drawbox(50, 50, 120, 120, color='red', thickness=5)
    .output('out.mp4')
    .run()
)
```

`ffmpeg-python` takes care of running `ffmpeg` with the command-line arguments that correspond to the above filter diagram, in familiar Python terms.

<img src="https://raw.githubusercontent.com/kkroening/ffmpeg-python/master/doc/screenshot.png" alt="Screenshot" align="middle" width="60%" />

Real-world signal graphs can get a heck of a lot more complex, but `ffmpeg-python` handles arbitrarily large (directed-acyclic) signal graphs.

## Installation

### Installing `ffmpeg-python`

The latest version of `ffmpeg-python` can be acquired via a typical pip install:

```bash
pip install ffmpeg-python
```

Or the source can be cloned and installed from locally:
```bash
git clone git@github.com:kkroening/ffmpeg-python.git
pip install -e ./ffmpeg-python
```

> **Note**: `ffmpeg-python` makes no attempt to download/install FFmpeg, as `ffmpeg-python` is merely a pure-Python wrapper - whereas FFmpeg installation is platform-dependent/environment-specific, and is thus the responsibility of the user, as described below.

### Installing FFmpeg

Before using `ffmpeg-python`, FFmpeg must be installed and accessible via the `$PATH` environment variable.

There are a variety of ways to install FFmpeg, such as the [official download links](https://ffmpeg.org/download.html), or using your package manager of choice (e.g. `sudo apt install ffmpeg` on Debian/Ubuntu, `brew install ffmpeg` on OS X, etc.).

Regardless of how FFmpeg is installed, you can check if your environment path is set correctly by running the `ffmpeg` command from the terminal, in which case the version information should appear, as in the following example (truncated for brevity):

```
$ ffmpeg
ffmpeg version 4.2.4-1ubuntu0.1 Copyright (c) 2000-2020 the FFmpeg developers
  built with gcc 9 (Ubuntu 9.3.0-10ubuntu2)
```

> **Note**: The actual version information displayed here may vary from one system to another; but if a message such as `ffmpeg: command not found` appears instead of the version information, FFmpeg is not properly installed.

## [Examples](https://github.com/kkroening/ffmpeg-python/tree/master/examples)

When in doubt, take a look at the [examples](https://github.com/kkroening/ffmpeg-python/tree/master/examples) to see if there's something that's close to whatever you're trying to do.

Here are a few:
- [Convert video to numpy array](https://github.com/kkroening/ffmpeg-python/blob/master/examples/README.md#convert-video-to-numpy-array)
- [Generate thumbnail for video](https://github.com/kkroening/ffmpeg-python/blob/master/examples/README.md#generate-thumbnail-for-video)
- [Read raw PCM audio via pipe](https://github.com/kkroening/ffmpeg-python/blob/master/examples/README.md#convert-sound-to-raw-pcm-audio)

- [JupyterLab/Notebook stream editor](https://github.com/kkroening/ffmpeg-python/blob/master/examples/README.md#jupyter-stream-editor)

<img src="https://raw.githubusercontent.com/kkroening/ffmpeg-python/master/doc/jupyter-demo.gif" alt="jupyter demo" width="75%" />

- [Tensorflow/DeepDream streaming](https://github.com/kkroening/ffmpeg-python/blob/master/examples/README.md#tensorflow-streaming)

<img src="https://raw.githubusercontent.com/kkroening/ffmpeg-python/master/examples/graphs/dream.png" alt="deep dream streaming" width="40%" />

See the [Examples README](https://github.com/kkroening/ffmpeg-python/tree/master/examples) for additional examples.

## Custom Filters

Don't see the filter you're looking for?  While `ffmpeg-python` includes shorthand notation for some of the most commonly used filters (such as `concat`), all filters can be referenced via the `.filter` operator:
```python
stream = ffmpeg.input('dummy.mp4')
stream = ffmpeg.filter(stream, 'fps', fps=25, round='up')
stream = ffmpeg.output(stream, 'dummy2.mp4')
ffmpeg.run(stream)
```

Or fluently:
```python
(
    ffmpeg
    .input('dummy.mp4')
    .filter('fps', fps=25, round='up')
    .output('dummy2.mp4')
    .run()
)
```

**Special option names:**

Arguments with special names such as `-qscale:v` (variable bitrate), `-b:v` (constant bitrate), etc. can be specified as a keyword-args dictionary as follows:
```python
(
    ffmpeg
    .input('in.mp4')
    .output('out.mp4', **{'qscale:v': 3})
    .run()
)
```

**Multiple inputs:**

Filters that take multiple input streams can be used by passing the input streams as an array to `ffmpeg.filter`:
```python
main = ffmpeg.input('main.mp4')
logo = ffmpeg.input('logo.png')
(
    ffmpeg
    .filter([main, logo], 'overlay', 10, 10)
    .output('out.mp4')
    .run()
)
```

**Multiple outputs:**

Filters that produce multiple outputs can be used with `.filter_multi_output`:
```python
split = (
    ffmpeg
    .input('in.mp4')
    .filter_multi_output('split')  # or `.split()`
)
(
    ffmpeg
    .concat(split[0], split[1].reverse())
    .output('out.mp4')
    .run()
)
```
(In this particular case, `.split()` is the equivalent shorthand, but the general approach works for other multi-output filters)

**String expressions:**

Expressions to be interpreted by ffmpeg can be included as string parameters and reference any special ffmpeg variable names:
```python
(
    ffmpeg
    .input('in.mp4')
    .filter('crop', 'in_w-2*10', 'in_h-2*20')
    .input('out.mp4')
)
```

<br />

When in doubt, refer to the [existing filters](https://github.com/kkroening/ffmpeg-python/blob/master/ffmpeg/_filters.py), [examples](https://github.com/kkroening/ffmpeg-python/tree/master/examples), and/or the [official ffmpeg documentation](https://ffmpeg.org/ffmpeg-filters.html).

## Frequently asked questions

**Why do I get an import/attribute/etc. error from `import ffmpeg`?**

Make sure you ran `pip install ffmpeg-python` and _**not**_ `pip install ffmpeg` (wrong) or `pip install python-ffmpeg` (also wrong).

**Why did my audio stream get dropped?**

Some ffmpeg filters drop audio streams, and care must be taken to preserve the audio in the final output.  The ``.audio`` and ``.video`` operators can be used to reference the audio/video portions of a stream so that they can be processed separately and then re-combined later in the pipeline.

This dilemma is intrinsic to ffmpeg, and ffmpeg-python tries to stay out of the way while users may refer to the official ffmpeg documentation as to why certain filters drop audio.

As usual, take a look at the [examples](https://github.com/kkroening/ffmpeg-python/tree/master/examples#audiovideo-pipeline) (*Audio/video pipeline* in particular).

**How can I find out the used command line arguments?**

You can run `stream.get_args()` before `stream.run()` to retrieve the command line arguments that will be passed to `ffmpeg`. You can also run `stream.compile()` that also includes the `ffmpeg` executable as the first argument.

**How do I do XYZ?**

Take a look at each of the links in the [Additional Resources](https://kkroening.github.io/ffmpeg-python/) section at the end of this README.  If you look everywhere and can't find what you're looking for and have a question that may be relevant to other users, you may open an issue asking how to do it, while providing a thorough explanation of what you're trying to do and what you've tried so far.

Issues not directly related to `ffmpeg-python` or issues asking others to write your code for you or how to do the work of solving a complex signal processing problem for you that's not relevant to other users will be closed.

That said, we hope to continue improving our documentation and provide a community of support for people using `ffmpeg-python` to do cool and exciting things.

## Contributing

<img align="right" src="https://raw.githubusercontent.com/kkroening/ffmpeg-python/master/doc/logo.png" alt="ffmpeg-python logo" width="20%" />

One of the best things you can do to help make `ffmpeg-python` better is to answer [open questions](https://github.com/kkroening/ffmpeg-python/labels/question) in the issue tracker.  The questions that are answered will be tagged and incorporated into the documentation, examples, and other learning resources.

If you notice things that could be better in the documentation or overall development experience, please say so in the [issue tracker](https://github.com/kkroening/ffmpeg-python/issues).  And of course, feel free to report any bugs or submit feature requests.

Pull requests are welcome as well, but it wouldn't hurt to touch base in the issue tracker or hop on the [Matrix chat channel](https://riot.im/app/#/room/#ffmpeg-python:matrix.org) first.

Anyone who fixes any of the [open bugs](https://github.com/kkroening/ffmpeg-python/labels/bug) or implements [requested enhancements](https://github.com/kkroening/ffmpeg-python/labels/enhancement) is a hero, but changes should include passing tests.

### Running tests

```bash
git clone git@github.com:kkroening/ffmpeg-python.git
cd ffmpeg-python
virtualenv venv
. venv/bin/activate  # (OS X / Linux)
venv\bin\activate    # (Windows)
pip install -e .[dev]
pytest
```

<br />

### Special thanks

- [Fabrice Bellard](https://bellard.org/)
- [The FFmpeg team](https://ffmpeg.org/donations.html)
- [Arne de Laat](https://github.com/153957)
- [Davide Depau](https://github.com/depau)
- [Dim](https://github.com/lloti)
- [Noah Stier](https://github.com/noahstier)

## Additional Resources

- [API Reference](https://kkroening.github.io/ffmpeg-python/)
- [Examples](https://github.com/kkroening/ffmpeg-python/tree/master/examples)
- [Filters](https://github.com/kkroening/ffmpeg-python/blob/master/ffmpeg/_filters.py)
- [FFmpeg Homepage](https://ffmpeg.org/)
- [FFmpeg Documentation](https://ffmpeg.org/ffmpeg.html)
- [FFmpeg Filters Documentation](https://ffmpeg.org/ffmpeg-filters.html)
- [Test cases](https://github.com/kkroening/ffmpeg-python/blob/master/ffmpeg/tests/test_ffmpeg.py)
- [Issue tracker](https://github.com/kkroening/ffmpeg-python/issues)
- Matrix Chat: [#ffmpeg-python:matrix.org](https://riot.im/app/#/room/#ffmpeg-python:matrix.org)
"""

DEFAULT_DOCKERFILE_FEW_SHOT_EXAMPLE = """# Use the official Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install FFmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Clone the ffmpeg-python repository
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    git clone https://github.com/kkroening/ffmpeg-python.git /app/ffmpeg-python && \
    rm -rf /var/lib/apt/lists/*

# Install the required dependencies
RUN pip install --no-cache-dir -r /app/ffmpeg-python/requirements.txt

# Optional: Set the entrypoint for the container
ENTRYPOINT ["python"]
"""
DEFAULT_DEVCONTAINER_JSON_FEW_SHOT_EXAMPLE = """{
    "name": "ffmpeg-python-dev-container",
    "dockerFile": "Dockerfile",
    "settings": {
        "terminal.integrated.shell.linux": "/bin/bash"
    },
    "extensions": [
        "ms-python.python"
    ],
    "forwardPorts": [],
    "postCreateCommand": "echo 'Welcome to your ffmpeg-python dev container!'"
}
"""

DEFAULT_SAMPLE_SCRIPT_FEW_SHOT_EXAMPLE = """
import requests
import ffmpeg
import tempfile

# Download a video file from the internet
video_url = 'https://download.samplelib.com/mp4/sample-5s.mp4'

response = requests.get(video_url, stream=True)
response.raise_for_status()

# Save the video to a temporary file
with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video_file:
    for chunk in response.iter_content(chunk_size=8192):
        temp_video_file.write(chunk)
    temp_video_file.flush()

    # Process the video using ffmpeg-python
    input_video = ffmpeg.input(temp_video_file.name)
    output_video = input_video.filter('scale', 320, 240).output('output_video.mp4')
    output_video.run()

print("Video processing completed. The output video is saved as output_video.mp4.")
"""

# Nextflow-Flyte Conversion few-shot examples

NF_TO_FLYTE_REPO_URL_FEW_SHOT_EXAMPLE = "https://github.com/richard-peacock/sequence_record_parsing"
NF_TO_FLYTE_README_FEW_SHOT_EXAMPLE = """# Sequence Record Parsing

Just a nextflow script that parses the `sample.fa` that my labmate keeps naming all his files.

This should probably all just be converted to a Flyte script in Python, but I'm not sure how to do that yet.
"""
NF_TO_FLYTE_DOCKERFILE_FEW_SHOT_EXAMPLE = """# Use nextflow/nextflow:22.10.8 as a base image
FROM nextflow/nextflow:22.10.8

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    sudo \
    python3.9 \
    python3-pip

RUN git clone https://github.com/mirand863/gcsplit.git && cd gcsplit && bash install.sh && source ~/.bashrc

# Install flytekit and scikit-learn
RUN pip3 install flytekit scikit-learn

# Install Flyte
RUN curl -sL https://ctl.flyte.org/install | sudo bash -s -- -b /usr/local/bin

"""
NF_TO_FLYTE_DEVCONTAINER_JSON_FEW_SHOT_EXAMPLE = """{
    "name": "nf-to-flyte-dev-container",
    "dockerFile": "Dockerfile",
    "settings": {
        "terminal.integrated.shell.linux": "/bin/bash"
    },
    "extensions": [
        "ms-python.python"
    ],
    "forwardPorts": [],
    "postCreateCommand": "echo 'Welcome to your nextflow-to-flyte dev container!'"
}
"""

NF_TO_FLYTE_SAMPLE_SCRIPT_FEW_SHOT_EXAMPLE = """import subprocess
from flytekit import task, workflow

@task
def split_sequences(file_path: str) -> str:
    SPLIT = 'gcsplit' if System.properties['os.name'] == 'Mac OS X' else 'csplit'
    # file_path = "~/sample.fa" would normally be an input argument
    output_prefix = 'seq_'
    # run the csplit command, storing the outputs in files with names prefixed by 'seq_'
    subprocess.check_output(f"{SPLIT} {file_path} '%^>%' '/^>/' '{{*}}' -f {output_prefix}", shell=True)
    return output_prefix

@task
def reverse(input_prefix: str) -> str:
    # use a shell command to get a list of all files that match the prefix
    files = subprocess.check_output(f"ls {input_prefix}*", shell=True).decode().split('\n')
    reversed_sequences = []
    # iterate through each file
    for f in files:
        if f:  # skip empty names
            # reverse the content of each file and store the result
            reversed_sequences.append(subprocess.check_output(f"cat {f} | rev", shell=True).decode())
    return "\n".join(reversed_sequences)

@workflow
def reverse_workflow(file_path: str) -> str:
    prefix = split_sequences(file_path=file_path)
    return reverse(input_prefix=prefix)

"""

# lucidrains/progen Conversion few-shot examples

LUCIDRAINS_PROGEN_REPO_URL_FEW_SHOT_EXAMPLE = "https://github.com/lucidrains/progen"
LUCIDRAINS_PROGEN_README_FEW_SHOT_EXAMPLE = """## ProGen - (wip)

Implementation and replication of <a href="https://arxiv.org/abs/2004.03497">ProGen</a>, Language Modeling for Protein Generation, in Pytorch and Jax (the weights will be made easily transferrable between the two). You can think of this as GPT for proteins sequences.

## Requirements

We are going to use <a href="https://github.com/python-poetry/poetry">Poetry</a> for managing the dependencies for this project. So first install it using the <a href="https://github.com/python-poetry/poetry#osx--linux--bashonwindows-install-instructions">one-liner bash command</a>.

Next, git clone the project and install the dependencies

```bash
$ git clone git@github.com:lucidrains/progen
$ cd progen
$ poetry install
```

For training on GPUs, you may need to rerun pip install with the correct CUDA version. You can follow the instructions <a href="https://github.com/google/jax#pip-installation-gpu-cuda">here</a>


```bash
# ex. CUDA 11.1
$ pip install --upgrade "jax[cuda111]" -f https://storage.googleapis.com/jax-releases/jax_releases.html
```

For running any scripts, you'll notice that it will always be prepended with `poetry run`

## Usage

```python
from jax import random
from haiku import PRNGSequence
from progen_transformer import ProGen

model = ProGen(
    num_tokens = 256,
    dim = 512,
    seq_len = 1024,
    window_size = 256,       # local attention window size
    depth = 12,              # depth
    heads = 8,               # attention heads
    dim_head = 64,           # dimension per head
    ff_glu = True,           # use GLU in feedforward, from Noam's paper
    global_mlp_depth = 2     # last N global gmlp layers
)

rng = PRNGSequence(42)
seq = random.randint(next(rng), (1024,), 0, 256)

params = model.init(next(rng), seq)
logits = model.apply(params, next(rng), seq) # (1024, 256)
```

## Training

Download Uniref50 from <a href="https://www.uniprot.org/downloads">UniProt</a> and place `uniref50.fasta` in the root directory

```bash
$ poetry run python generate_data.py
```

You should see a lot of green if everything succeeds. Then


```bash
$ poetry run python train.py
```

By default, the script will checkpoint and resume automatically, but if you wish to clear your progress and restart, just add a `--new` flag

```bash
$ poetry run python train.py --new
```

Model checkpoints will be saved periodically to `./ckpts`

Finally, to sample from your checkpoint, just do

```bash
$ poetry run python sample.py
```

You can pass a prime with `--prime`. You can either pass the annotations, followed by `#`, to get the generated sequence, or pass the sequence (also followed by `#`) and get the generated annotations

```bash
$ poetry run python sample.py --prime "[Tax=Mammalia] #"
```

## Mixed Precision

To use mixed precision training, you'll need to install the latest Haiku with the following command

```bash
$ pip install git+https://github.com/deepmind/dm-haiku
```

Then make sure to set the `--mixed_precision` flag when invoking the training script

```bash
$ poetry run python train.py --mixed_precision
```

## Todo

- [ ] model parallelism with pjit
- [ ] join in GO annotations with pandas dataframe
- [ ] setup annotation -> template string system, all configuration driven, find easy way to test. offer two types of annotations, one parsed from uniref descriptions, the other from GO annotation presence
- [ ] add multiple data sources (check out trembl)
- [ ] when sampling, prime with entire sequence prior to the pound sign (intersection of sequence and annotation)
- [ ] utilize all cores when processing data
- [ ] save all training settings in the checkpoints too
- [x] bfloat16 on xla
- [x] resume from correct place in tfrecord even if batch size is changed inbetween runs, display number of sequences processed
- [x] train compressed gzip tfrecords from google cloud storage path
- [x] remove tfrecord package and just use tfrecordwriter with gzip
- [x] generate validation tfrecords
- [x] checkpoint and resume from a google cloud storage path
- [x] use jinja2 for wandb html sample logging
- [x] manage experimental tracker state, and also allow ability to turn it off by piping to noop
- [x] add a confirmation before clearing a folder for --new run
- [x] engineer mask in cross entropy loss so that padding can be reused as end-of-string token
- [x] flip seq # annotation order with prob set in config
- [x] keep N last checkpoints

## Acknowledgements

Many thanks goes out to <a href="https://github.com/kingoflolz">Ben Wang</a>, who showed this type of large-scale training can be achieved with <a href="https://github.com/kingoflolz/mesh-transformer-jax">GPT-J</a>

## Citations

```bibtex
@misc{madani2020progen,
    title   = {ProGen: Language Modeling for Protein Generation}, 
    author  = {Ali Madani and Bryan McCann and Nikhil Naik and Nitish Shirish Keskar and Namrata Anand and Raphael R. Eguchi and Po-Ssu Huang and Richard Socher},
    year    = {2020},
    eprint  = {2004.03497},
    archivePrefix = {arXiv},
    primaryClass = {q-bio.BM}
}
```

```bibtex
@misc{su2021roformer,
    title   = {RoFormer: Enhanced Transformer with Rotary Position Embedding},
    author  = {Jianlin Su and Yu Lu and Shengfeng Pan and Bo Wen and Yunfeng Liu},
    year    = {2021},
    eprint  = {2104.09864},
    archivePrefix = {arXiv},
    primaryClass = {cs.CL}
}
```

```bibtex
@misc{shazeer2020glu,
    title   = {GLU Variants Improve Transformer},
    author  = {Noam Shazeer},
    year    = {2020},
    url     = {https://arxiv.org/abs/2002.05202}
}
```
"""
LUCIDRAINS_PROGEN_DOCKERFILE_FEW_SHOT_EXAMPLE = """# Use an official Python runtime as a parent image
FROM python:3.9-alpine

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install system level dependencies
RUN apk add --no-cache gcc musl-dev git

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | sh

# Clone the ProGen project
RUN git clone https://github.com/lucidrains/progen.git

# Change to the project directory
WORKDIR /progen

# Install the project dependencies
RUN poetry install

# Install the latest Haiku for mixed precision training
RUN pip install git+https://github.com/deepmind/dm-haiku

# Install the correct CUDA version for GPU training
# Note: This is commented out because Alpine doesn't support CUDA. If you need CUDA support, consider using an Ubuntu-based image.
# RUN pip install --upgrade "jax[cuda111]" -f https://storage.googleapis.com/jax-releases/jax_releases.html

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME ProGen

# Run the application when the container launches
CMD ["poetry", "run", "python", "sample_script.py"]
"""
LUCIDRAINS_PROGEN_DEVCONTAINER_JSON_FEW_SHOT_EXAMPLE = """{
    "name": "ProGen Dev Containerrr",
    "dockerFile": "../Dockerfile",
    "forwardPorts": [80],
    "settings": {
        "terminal.integrated.shell.linux": "/bin/sh"
    },
    "extensions": [
        "ms-python.python"
    ],
    "remoteUser": "root",
    "postCreateCommand": "echo 'Container is ready!'"
}
"""

LUCIDRAINS_PROGEN_SAMPLE_SCRIPT_FEW_SHOT_EXAMPLE = """from jax import random
from haiku import PRNGSequence
from progen_transformer import ProGen
import jax

model = ProGen(
    num_tokens = 256,
    dim = 512,
    seq_len = 1024,
    window_size = 256,       # local attention window size
    depth = 12,              # depth
    heads = 8,               # attention heads
    dim_head = 64,           # dimension per head
    ff_glu = True,           # use GLU in feedforward, from Noam's paper
    global_mlp_depth = 2     # last N global gmlp layers
)

rng = PRNGSequence(42)
seq = random.randint(next(rng), (1024,), 0, 256)

params = model.init(next(rng), seq)
logits = model.apply(params, next(rng), seq) # (1024, 256)
print('Hello! ProGen model:')
print(model)
# Define your model parameters
model_params = {
    'num_tokens': 10000,  # Number of tokens in your vocabulary
    'dim': 512,  # Dimension of the model
    'seq_len': 256,  # Length of the sequence
    'depth': 6,  # Number of layers in the model
    'window_size': 256,  # Size of the attention window
    'global_mlp_depth': 2,  # Depth of the global MLP
    'heads': 8,  # Number of attention heads
    'dim_head': 64,  # Dimension of each attention head
    'ff_mult': 4,  # Multiplier for the feed-forward network dimension
    'ff_glu': True,  # Whether to use GLU in the feed-forward network
    'attn_dim': None,  # Dimension of the attention mechanism
    'clamp_gate': True,  # Whether to clamp the gate
    'shift_tokens': True  # Whether to shift tokens
}

# Create an instance of the model
model = ProGen(**model_params)

# Initialize the model with some random input
rng = jax.random.PRNGKey(42)
input_seq = jax.random.randint(rng, (256,), 0, 10000)  # Random sequence of length 256
params = model.init(rng, input_seq)

# Flatten the parameters
params_flat, _ = jax.tree_flatten(params)

# Print the shapes
print('The shapes')
for param in params_flat:
    print(param.shape)

"""
