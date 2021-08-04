
import { faCalendarCheck, faComment } from '@fortawesome/free-solid-svg-icons';

import Profile1 from "../assets/img/team/profile-picture-1.jpg"
import Profile2 from "../assets/img/team/profile-picture-2.jpg"
// import Profile3 from "../assets/img/team/profile-picture-3.jpg"
// import Profile4 from "../assets/img/team/profile-picture-4.jpg"
import DuyProfile from "../assets/img/team/duy.JPG"

export default [
    {
        "id": 1,
        "image": Profile1,
        "name": "Professor - Nghia Nguyen",
        "statusKey": "online",
        "icon": faCalendarCheck,
        "btnText": "Invite"
    },
    {
        "id": 2,
        "image": Profile2,
        "name": "Kai - Hung Le",
        "statusKey": "inMeeting",
        "icon": faComment,
        "btnText": "Message"
    },
    {
        "id": 3,
        "image": DuyProfile,
        "name": "Pot - Duy Nguyen",
        "statusKey": "offline",
        "icon": faCalendarCheck,
        "btnText": "Invite"
    },
    // {
    //     "id": 4,
    //     "image": Profile4,
    //     "name": "Neil Sims",
    //     "statusKey": "online",
    //     "icon": faComment,
    //     "btnText": "Message"
    // }
]