# Copyright (C) 2026 Matthew Jones and Andrea Rajšić
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
 
import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression


def logistic_crossover_estimate(
    df: pd.DataFrame,
    random_seed: int = 0,
    C_logistic: float = 1e5,
    return_model: bool = False,
    **kwargs
) -> tuple:
  """
  Estimates regolith thickness from input `df` of REC and nREC craters based on the crossover
  excavation depth (0.084*D), i.e. the depth at which there is 50% probability of being a REC.

  Parameters:
  ----------
  df : pd.DataFrame
    DataFrame of undegraded craters with at least the following columns:
    - 'exc_depth': Excavation depth of the crater [m]
    - 'is_REC': 0 = nREC, 1 = REC
  random_seed : int, optional
    Random seed for reproducibility. Default is 0.
  C_logistic : float, optional
    Inverse of regularization strength for logistic regression. Default is 1e5 (effectively no regularization).
  return_model : bool, optional
    If True, also return the fitted logistic regression model. Default is False.
  kwargs : additional keyword arguments or dict
    Additional keyword arguments to pass to LogisticRegression.
  
  Returns:
  -------
  crossover : float
    Estimated regolith thickness at which the probability of being a REC is 50%.
  model : LogisticRegression
    The fitted logistic regression model (only returned if return_model=True).
  """
  # Retrieve features and target variable
  X = df[['exc_depth']].values
  y = df['is_REC'].astype(int).values
  # Fit logistic regression model
  clf_log = LogisticRegression(random_state=random_seed, C=C_logistic, **kwargs)
  clf_log.fit(X, y)
  # Calculate crossover point where probability of being a REC is 50%
  b0_log = clf_log.intercept_[0]
  b1_log = clf_log.coef_[0][0]
  crossover = -b0_log / b1_log if (b1_log != 0) else np.nan
  # Return results
  if return_model:
    return crossover, clf_log
  else:
    return crossover