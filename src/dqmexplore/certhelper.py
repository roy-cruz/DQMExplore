from dqmexplore.utils.datautils import loadJSONasDF, loadFromWeb
from fnmatch import fnmatch
import pandas as pd

class CHRunData:
    """
    Class to organize the Reference Runs information from the CertHelper API
    Credit for original JSON implementation: Gabriele Benelli
    """

    def __init__(self, JSONFilePath, goldenJSONFilePath=None, filtergolden=True):
        self.RunsDF = loadJSONasDF(JSONFilePath)
        self.RunsDF.dropna(inplace=True)
        self._setGolden(goldenJSONFilePath)
        self.RunsDF.sort_values("run_number", inplace=True)

    def _setGolden(self, goldenJSONFilePath=None):
        if goldenJSONFilePath is None:
            return
        self.goldenDF = loadJSONasDF(goldenJSONFilePath)
        self.goldenDF = self.goldenDF.rename(
            {0: "run_number", 1: "good_lss"}, axis=1
        )
        self.goldenDF = self.goldenDF.astype({"run_number": int})

        # Put golden info in RunsDF
        self.RunsDF = self.RunsDF.merge(self.goldenDF, on="run_number", how="left")
        self.RunsDF["good_lss"] = self.RunsDF["good_lss"].where(self.RunsDF["good_lss"].notna(), None)

    def getGoodRuns(self):
        return self.RunsDF[self.RunsDF["good_lss"].notnull()]

    def getRuns(self, exclude_bad=True):
        if exclude_bad:
            return self.getGoodRuns()
        else:
            return self.RunsDF

    def getRun(self, runnb):
        return self.RunsDF[self.RunsDF["run_number"] == runnb]

    def applyFilter(self, exclude_bad=True, filters={}):
        if exclude_bad:
            RunsDF = self.getGoodRuns()
        else: 
            RunsDF = self.RunsDF

        if len(filters) == 0:
            print("Warning: No filter conditions given.")
            return RunsDF

        mask = pd.Series([True] * len(RunsDF), index=RunsDF.index)

        for key, value in filters.items():
            if key in ["run_number", "reference_run_number"]: # must be list of ints and/or tuples
                num_mask = pd.Series([False] * len(RunsDF), index=RunsDF.index)
                for val in value:
                    if isinstance(val, tuple):
                        num_mask |= (RunsDF[key] >= val[0]) & (RunsDF[key] <= val[1])
                    elif isinstance(val, (int, float)):
                        num_mask |= RunsDF[key] == val
                mask &= num_mask
            elif isinstance(value, str) and key in [
                "run_reconstruction_type",
                "reference_run_reconstruction_type",
                "dataset",
            ]:
                mask &= RunsDF[key].apply(lambda x: fnmatch(x, value))
        return RunsDF[mask]

    def getruns(self, run, colfilters=None):
        CHftrs = [
            "run_number",
            "run_reconstruction_type",
            "reference_run_type",
            "reference_run_reconstruction_type",
            "dataset",
        ]
        try:
            runs = self.RunsDF[self.RunsDF["run_number"] == run]
            if colfilters is None:
                return runs
            else:
                if isinstance(colfilters, list):
                    badftrs = []
                    for colfilter in colfilters:
                        if colfilter not in CHftrs:
                            badftrs.append(colfilter)
                            print(
                                "WARNING: {} not a valid CH feature. Skipping.".format(
                                    colfilter
                                )
                            )
                    return runs[list(set(colfilters) - set(badftrs))]
                else:
                    raise Exception("colfilters must be of type list")
        except:
            raise Exception("Run is not available.")