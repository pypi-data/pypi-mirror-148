// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React from "react";
import { Feed, Container } from "semantic-ui-react";
import PropTypes from "prop-types";

// Wrapper component for the custom styles being used inside the request events timeline
// Enables centralizing the styles and abstracts it away from the template
export const RequestsFeed = ({ children }) => (
  <Container className="requests-feed-container">
    <Feed>{children}</Feed>
  </Container>
);

export const RequestEventItem = ({ children }) => (
  <div className="requests-event-item">
    <div className="requests-event-container">{children}</div>
  </div>
);

export const RequestEventInnerContainer = ({ children }) => (
  <div className="ui feed requests-event-inner-container">{children}</div>
);

export const RequestEventAvatarContainer = ({ children }) => (
  <div className="requests-avatar-container">{children} </div>
);

export const RequestEventItemIconContainer = ({ children }) => (
  <div className="requests-action-event-icon"> {children} </div>
);

export const RequestEventItemBody = ({ isActionEvent, ...props }) => (
  <Feed.Event
    {...props}
    className={isActionEvent ? "requests-action-event" : ""}
  />
);

RequestEventItemBody.propTypes = {
  isActionEvent: PropTypes.bool,
};
RequestEventItemBody.defaultProps = {
  isActionEvent: false,
};

RequestsFeed.InnerContainer = RequestEventInnerContainer;
RequestsFeed.AvatarContainer = RequestEventAvatarContainer;
RequestsFeed.IconContainer = RequestEventItemIconContainer;
RequestsFeed.Item = RequestEventItem;
RequestsFeed.Event = RequestEventItemBody;

export default RequestsFeed;
