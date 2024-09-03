# (c) 2024 Copyright, Real-Time Innovations, Inc.  All rights reserved.
# No duplications, whole or partial, manual or electronic, may be made
# without express written permission.  Any such copies, or revisions thereof,
# must display this notice unaltered.
# This code contains trade secrets of Real-Time Innovations, Inc.
FROM quay.io/pypa/manylinux2010_x86_64:2021-02-06-3d322a5

ARG USER_NAME=jenkins
ARG USER_UID

RUN adduser $USER_NAME -u $USER_UID

RUN yum update -y && yum install -y openssl-devel

# Terrible workaround to install an old Rust version, this glibc is not compatible with the latest
# RUN curl -sSf https://static.rust-lang.org/rustup/archive/1.22.1/x86_64-unknown-linux-gnu/rustup-init -o rustup-init \
#     && chmod 755 rustup-init \
#     && ./rustup-init -y
# ENV PATH=/root/.cargo/bin:$PATH
# RUN /root/.cargo/bin/rustup install 1.49.0 | tee log
# ENV PATH=/root/.rustup/toolchains/1.49.0-x86_64-unknown-linux-gnu/bin/:$PATH

# Install Python dependencies
RUN /opt/python/cp35-cp35m/bin/pip install --upgrade pip
RUN /opt/python/cp35-cp35m/bin/pip install cmake==3.12.0 wheel twine

ENV PATH=/home/jenkins/.local/bin:$PATH
ENV PATH=/opt/python/cp27-cp27m/bin:$PATH
ENV PATH=/opt/python/cp35-cp35m/bin:$PATH
ENV PATH=/opt/python/cp36-cp36m/bin:$PATH
