FROM python:3.7
RUN pip3 install \
    voila \
    ipywidgets numpy matplotlib plotly

# create a user, since we don't want to run as root
RUN useradd -m ipst
ENV HOME=/home/ipst
WORKDIR $HOME
USER ipst

COPY --chown=jovyan:jovyan entrypoint.sh /home/ipst
COPY --chown=jovyan:jovyan test_voila.ipynb /home/ipst

EXPOSE 8888

ENTRYPOINT ["/home/ipst/entrypoint.sh"]