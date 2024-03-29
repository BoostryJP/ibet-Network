FROM ubuntu:22.04

# make application directory
RUN mkdir -p /app/ibet-Network/

# add apl user/group
RUN groupadd -g 1000 apl \
 && useradd -g apl -s /bin/bash -u 1000 -p apl apl \
 && echo 'apl ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers \
 && chown -R apl:apl /app

# install packages
RUN apt-get update -q \
 && apt-get install -y --no-install-recommends \
 build-essential \
 ca-certificates \
 libbz2-dev \
 libreadline-dev \
 libsqlite3-dev \
 libssl-dev \
 zlib1g-dev \
 libffi-dev \
 python3-dev \
 libpq-dev \
 automake \
 pkg-config \
 libtool \
 libgmp-dev \
 language-pack-ja-base \
 language-pack-ja \
 git \
 curl \
 libyaml-cpp-dev \
 liblzma-dev

# remove unnessesory package files
RUN apt clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# install pyenv
RUN git clone https://github.com/pyenv/pyenv.git /home/apl/.pyenv
RUN chown -R apl:apl /home/apl

USER apl
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~apl/.bash_profile \
 && echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~apl/.bash_profile \
 && echo 'eval "$(pyenv init --path)"' >> ~apl/.bash_profile \
 && echo 'export LANG=ja_JP.utf8' >> ~apl/.bash_profile

# install python
USER apl
RUN . ~/.bash_profile \
 && pyenv install 3.11.2 \
 && pyenv global 3.11.2 \
 && pip install --upgrade pip setuptools

# install poetry
RUN . ~/.bash_profile \
 && python -m pip install poetry==1.7.1
RUN . ~/.bash_profile \
 && poetry config virtualenvs.create false

# install python packages
USER root
COPY . /app/ibet-Network/tests
RUN chown -R apl:apl /app/ibet-Network/tests \
 && find /app/ibet-Network/tests/ -type d -name __pycache__ | xargs rm -fr \
 && chmod 755 /app/ibet-Network/tests

# install python packages
USER apl
RUN . ~/.bash_profile \
 && cd /app/ibet-Network/tests \
 && poetry install --no-root \
 && rm -f /app/ibet-Network/tests/pyproject.toml \
 && rm -f /app/ibet-Network/tests/poetry.lock

ENV PYTHONPATH /app/ibet-Network/tests

USER apl
CMD tail -f /dev/null