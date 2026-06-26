import { useEffect, useState } from "react";

const STORAGE_KEY = "talentmosaic_models";

function getInitialModels() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);

    if (!saved) {
      return {
        lastModel: null,
        models: [],
      };
    }

    return JSON.parse(saved);
  } catch {
    return {
      lastModel: null,
      models: [],
    };
  }
}

export function useModelStore() {
  const [state, setState] = useState(getInitialModels);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }, [state]);

  const saveModel = (model) => {
    setState((currentState) => {
      const exists = currentState.models.some(
        (item) => item.model_id === model.model_id
      );

      const models = exists
        ? currentState.models
        : [model, ...currentState.models];

      return {
        lastModel: model,
        models,
      };
    });
  };

  const clearModels = () => {
    setState({
      lastModel: null,
      models: [],
    });
  };

  return {
    lastModel: state.lastModel,
    models: state.models,
    saveModel,
    clearModels,
  };
}