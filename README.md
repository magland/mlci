# MountainLab continuous integration (mlci)

This is a service that is meant to be run in a Docker container somewhere.

## Deploying to heroku

After cloning this repo, create a kbucket share to share the contents of the `output/` directory (which will be inside the container)

```
cd output
kbucket-share .
```

Answer the questions to create the share, and then after it has successfully connected, `ctrl+c` to close the share. Make a note of the kbucket node id (you will need it below). It is important for the contents of the `output/.kbucket` directory to go into the container... but this should not be committed into the source repo.

Now deploy to heroku (assume you have a heroku account and there exists a heroku app called mlci):

```
heroku login
heroku container:login
```

Build and push the docker image:

```
cd mlci
heroku container:push worker -a mlci
heroku container:release worker -a mlci
```

Now the service should be running on heroku. To check what's going on, do:

```
heroku logs -a mlci
```

The service will generate a status.html file every minute or so, and it can be viewed at `https://kbucket.flatironinstitute.org/[kbucket-node-id]/download/status.html`, where you must replace `[kbucket-node-id]` with the appropriate kbucket node id.

For example: [https://kbucket.flatironinstitute.org/c1843dd95d9a/download/status.html](https://kbucket.flatironinstitute.org/c1843dd95d9a/download/status.html).
