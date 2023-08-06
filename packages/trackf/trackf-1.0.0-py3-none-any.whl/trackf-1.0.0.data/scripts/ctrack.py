"""Tracking the timeframe, Molecule Identifier,
and lengths of polymer chains at break."""


import csv
import warnings
import numpy as np
from netCDF4 import Dataset
import matplotlib.pylab as plt
from scipy.stats import gaussian_kde

warnings.filterwarnings("ignore")


def default_M(fname):
    """Calculate default value of number of chains (M)
    by finding the unique molecular identifier."""
    ds = Dataset(fname, "r")
    M0 = int(np.unique(ds["mol"][:]).shape[0])
    return M0


def getbreak(fname, M):
    """Get information about chain breaking.
    ----------------------------------------
    By monitoring the potential energy of the atoms, we can define
    the chain ends. Then, we store this information for each molecule
    at all timeframe. The mismatch between the precedent and the
    subsequent length indicate when and where the scission occur.
    """
    # First, import the data
    ds = Dataset(fname, "r")
    nf = np.shape(ds["time"][:])[0]  # number of timeframe
    track = []
    n = 0  # accounts for the first run so we can vstack rows of "track"

    for tf in range(nf):
        be = ds["c_be"][tf, :]
        mol = np.repeat(np.arange(M), M)

        # Counts atoms in each segment
        cee = (np.min(be[np.nonzero(be)]) + np.median(be)) / 2
        # cee is a threshold value below which atoms are at chain ends
        inde = np.array(np.where(be < cee))  # index chain ends
        ind0 = np.array(np.where(inde == np.where(be == 0)[0]))[1:]
        # Zero potential energy = single atoms
        for ind00 in ind0:
            inde = np.insert(inde, ind00, 0)
            inde[ind00 + 1] = 0
        inde = inde.reshape(int(np.size(inde) / 2), 2)
        idmol = mol[inde[:, 0]]
        cl = inde[:, 1] - inde[:, 0] + 1  # +1 for the number of atoms

        if tf == 0:
            idmol1 = idmol
            cl1 = cl
            tf1 = tf

        # Now bring them all together
        for m in range(M):
            cldis2 = np.setdiff1d(cl[idmol == m], cl1[idmol1 == m])
            cldis1 = np.setdiff1d(cl1[idmol1 == m], cl[idmol == m])
            u2, c2 = np.unique(cl[idmol == m], return_counts=True)
            u1, c1 = np.unique(cl1[idmol1 == m], return_counts=True)

            if np.setdiff1d(u2[c2 > 1], u1[c1 > 1]).shape[0] != 0:
                diff = np.setdiff1d(u2[c2 > 1], u1[c1 > 1])
                cldis2 = np.append(cldis2, diff)

            if np.size(cldis1 != 0):
                row = [m, tf1, cldis1, tf, cldis2]
                if n == 0:
                    track = row
                else:
                    track = np.vstack((track, row))
                n += 1

        # Store values for comparing with the values from the next time frame
        idmol1 = idmol
        cl1 = cl
        tf1 = tf

    # Close dump file
    ds.close()
    return track


def getsite(fname, M):
    """
    Calculate the location of breakage (bloc)
    in relation to its length
    1 > bloc > 0 where 0,1 indicates chain ends and 0.5 is midchain
    ----------------------------------------
    There are three scenarios we have to consider:
    1) Two segments of an original molecule break at the same time;
    each breaks into 2 segments
    2) Two segments of an original molecule break at the same time;
    eack breaks into >= 2 segments
    3) Only a segment of an original molecule breaks.
    """
    track = getbreak(fname, M)
    bloc = []
    tframe = []  # Timeframe
    # location and timeframe at break
    for arow in track:
        if arow[2].shape[0] > 1:  # Scenario 1
            for l1 in arow[2]:
                diff = [l1 - l2 for l2 in arow[4]]
                # Scenario 1
                if np.intersect1d(diff, arow[4]).shape[0] != 0:
                    l2 = np.intersect1d(diff, arow[4])
                    bloc = np.append(bloc, l2 / l1)
                    # Scenario 2
                    if arow[4].shape[0] > 4:
                        l3 = np.setdiff1d(arow[2], l1)
                        l4 = np.setdiff1d(arow[4], l2)
                        if sum(l4) != l3[0]:
                            l4 = np.append(l4, l3 - sum(l4))
                        bloc = np.append(bloc, l4 / l3)
        # Scenario 3
        else:
            bloc = np.append(bloc, arow[4] / arow[2][0])
        tframe = np.append(tframe, np.repeat(arow[1], arow[4].shape[0]))
    return np.vstack((tframe, bloc)).T


def plotdensity(fname, M):
    """Plot 2-D density plot of fracture sites.
    Gaussian_kde function will allow us to visualize the heatmap of
    the fracture sites.
    """
    data = getsite(fname, M)
    data = data.T
    stat = gaussian_kde(data)(data)

    plt.scatter(data[0, :], data[1, :], c=stat, s=100, cmap="viridis")
    plt.xlabel("Time Frame")
    plt.ylabel(r"Fracture Location ($f_{bl}$)")
    # plt.savefig(fpath + "/fracture_site_distribution.svg")
    return plt.show()


def file_to_csv(func, fpath):
    """Output result as a csv file."""
    if func.shape[1] == 5:
        fname = "fracture_site_distribution"
        func = np.append(
            np.array(
                [
                    ["Molecule Identifier"],
                    ["Time Frame 1"],
                    ["Length 1"],
                    ["Time Frame 2"],
                    ["Length 2"],
                ]
            ).T,
            func,
            axis=0,
        )
    else:
        fname = "fracture_site"
        func = np.append(
            np.array([["Time Frame"], ["Fracture Location"]]).T, func, axis=0
        )
    with open(fpath + fname + ".csv", "w", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(func.tolist())
    return print(fpath + fname + ".csv")


def sitehist(fname, M):
    """Output a histogram of the fracture sites."""
    site = getsite(fname, M)
    he, xe = np.histogram(site[:, 1], bins=100, density=True)
    plt.plot(xe[:-1], he)
    plt.xlabel(r"Fracture Site ($f_{bl}$)")
    plt.ylabel(r"P($f_{bl}$)")
    plt.show()
    return print("Fracture Site Distribution")


# end
