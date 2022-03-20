import os
from env import Environment


class Defaults():
    # set default image

    def setDefaultImage(request, userType):
        # default profile picture
        # adding default image
        if userType == 'admin':
            if request.profile_picture is None or len(request.profile_picture) == 0:
                image = 'admin.png'
            else:
                image = request.profile_picture

            return image
        else:
            if request.profile_picture is None or len(request.profile_picture) == 0:
                image = 'user.png'
            else:
                image = request.profile_picture

            return image

    # set default image for user
    def getDefaultImage(user, userType):
        # default profile picture
        if userType == 'user':
            if user.profile_picture is not None and len(user.profile_picture) != 0:
                path = f"{Environment.getBaseEnv()}assets/profiles/user/{user.profile_picture}"
                default_image = path
                isExist = path
                if not isExist:
                    default_image = f"{Environment.getBaseEnv()}defaults/user.png"

            else:
                default_image = f"{Environment.getBaseEnv()}defaults/user.png"

            return default_image

        else:
            if user.profile_picture is not None and len(user.profile_picture) != 0:
                path = f"{Environment.getBaseEnv()}assets/profiles/admin/{user.profile_picture}"
                default_image = path
                isExist = path
                if not isExist:
                    default_image = f"{Environment.getBaseEnv()}defaults/admin.png"

            else:
                default_image = f"{Environment.getBaseEnv()}defaults/admin.png"

            return default_image
