# (c) 2024 Copyright, Real-Time Innovations, Inc.  All rights reserved.
# No duplications, whole or partial, manual or electronic, may be made
# without express written permission.  Any such copies, or revisions thereof,
# must display this notice unaltered.
# This code contains trade secrets of Real-Time Innovations, Inc.
FROM quay.io/pypa/manylinux2010_x86_64:2021-02-06-3d322a5

ARG USER_NAME=jenkins
ARG USER_UID

RUN adduser $USER_NAME -u $USER_UID
RUN /opt/python/cp36-cp36m/bin/pip install cmake==3.12.0 wheel

ENV PATH=/home/jenkins/.local/bin:$PATH
ENV PATH=/opt/python/cp27-cp27m/bin:$PATH
ENV PATH=/opt/python/cp36-cp36m/bin:$PATH
