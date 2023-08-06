// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React from "react";
import TimelineActionEvent from "../components/TimelineActionEvent";

export const TimelineAcceptEvent = ({ event }) => (
  <TimelineActionEvent
    iconName="check circle"
    iconColor={"green"}
    event={event}
  />
);

export const TimelineDeclineEvent = ({ event }) => (
  <TimelineActionEvent iconName="close" event={event} iconColor="red" />
);

export const TimelineExpireEvent = ({ event }) => (
  <TimelineActionEvent
    iconName="calendar times"
    event={event}
    userAction={false}
    iconColor="red"
  />
);

export const TimelineCancelEvent = ({ event }) => (
  <TimelineActionEvent iconName="close" event={event} iconColor="red" />
);
