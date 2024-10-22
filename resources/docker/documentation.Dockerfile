# (c) 2024 Copyright, Real-Time Innovations, Inc.  All rights reserved.
# No duplications, whole or partial, manual or electronic, may be made
# without express written permission.  Any such copies, or revisions thereof,
# must display this notice unaltered.
# This code contains trade secrets of Real-Time Innovations, Inc.
FROM python:3.6

ARG USER_NAME=jenkins
ARG USER_UID

RUN adduser $USER_NAME -u $USER_UID
ENV PATH=/home/jenkins/.local/bin:$PATH

RUN pip install cmake==3.12.0

RUN mkdir -p /tmp/awscli/ \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscli/awscliv2.zip" \
    && unzip /tmp/awscli/awscliv2.zip -d /tmp/awscli \
    && /tmp/awscli/aws/install \
    && rm -rf /tmp/awscli
