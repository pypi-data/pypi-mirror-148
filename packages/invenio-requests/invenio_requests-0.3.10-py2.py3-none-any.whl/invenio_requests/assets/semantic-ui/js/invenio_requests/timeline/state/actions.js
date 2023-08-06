// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

export const IS_LOADING = "timeline/IS_LOADING";
export const SUCCESS = "timeline/SUCCESS";
export const HAS_ERROR = "timeline/HAS_ERROR";
export const IS_REFRESHING = "timeline/REFRESHING";
export const CHANGE_PAGE = "timeline/CHANGE_PAGE";

const mockedRequestStatusEvents = [
  {
    id: "dasf33d23dsd",
    payload: {
      content: "<p> accepted the invitation 2 days go</p>",
      format: "html",
    },
    created_at: "2021-10-28T20:30.212323",
    type: "A",
    created_by: { user: "1", name: "John Doe" },
    updated_at: "2021-10-28T20:31.212323",
    links: {},
    revision_id: 1,
  },
];

class intervalManager {
  static IntervalId = undefined;

  static setIntervalId(intervalId) {
    this.intervalId = intervalId;
  }
}

export const fetchTimeline = (loadingState = true) => {
  return async (dispatch, getState, config) => {
    const state = getState();
    const { size, page } = state.timeline;

    if (loadingState) {
      dispatch({
        type: IS_LOADING,
      });
    }
    dispatch({
      type: IS_REFRESHING,
    });

    try {
      const response = await config.requestsApi.getTimeline({
        size: size,
        page: page,
        sort: "oldest",
      });

      const dataWithMock = (data) => {
        data.hits.hits = data.hits.hits.concat(mockedRequestStatusEvents);
        data.hits.hits.push(data.hits.hits[0])


        return data;
      };

      dispatch({
        type: SUCCESS,
        payload: dataWithMock(response.data),
      });
    } catch (error) {
      dispatch({
        type: HAS_ERROR,
        payload: error,
      });
    }
  };
};

export const setPage = (page) => {
  return async (dispatch, getState, config) => {
    dispatch({
      type: CHANGE_PAGE,
      payload: page,
    });

    dispatch(fetchTimeline());
  };
};

const timelineReload = (dispatch, getState, config) => {
  const state = getState();
  const { loading, refreshing, error } = state.timeline;
  const { isLoading: isSubmitting } = state.timelineCommentEditor;

  const intervalId = intervalManager.intervalId;
  if (error) {
    // stop requesting if error
    clearInterval(intervalId);
  }

  // avoid concurrent requests if the previous one did not finish
  return (
    !loading && !refreshing && !isSubmitting && dispatch(fetchTimeline(false))
  );
};

export const getTimelineWithRefresh = () => {
  return async (dispatch, getState, config) => {
    dispatch(fetchTimeline(true));

    const intervalAlreadySet = intervalManager.intervalId;

    if (!intervalAlreadySet) {
      const intervalId = setInterval(
        () => timelineReload(dispatch, getState, config),
        config.refreshIntervalMs
      );
      intervalManager.setIntervalId(intervalId);
    }
  };
};

export const timelineStopRefresh = () => {
  return (dispatch, getState, config) => {
    const intervalId = intervalManager.intervalId;
    clearInterval(intervalId);
  };
};
