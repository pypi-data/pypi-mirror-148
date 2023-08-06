import numpy as np
import datetime as DT
import warnings, glob, os, shutil
import pickle as pickle
import netCDF4 as nc
import f90nml
import collections
from subprocess import check_output

from testbedutils import dirtLib
from erdcIO import base

class swashio(base):  # actually write SWS file
    def __init__(self, fNameBase, **kwargs):
        """

        Args:
            fileNameBase:
            **kwargs:
        """
        self.modelName = 'swash'  # model name needs to be before base init (used in base init)
        super(swashIO, self).__init__(fNameBase, **kwargs)
        # this was removedbecause it would caue sand overwrite of input
        # self._replaceDefaultParams()

    def _replaceDefaultParams(self):
        """holds all default physical parameters settings for the entire model set """

        ## put check in place to make sure all values are used that are input into the newModelParams dictionary
        # set values with kwargs.get('string', value)
        # print list of values that are acceptable if any new model param is not used

        print('TODO: Replacing parameters.... what''s left can be warned at the end of '
              'this process [wrr.swashIO_replaceDefaultParams]')

        # SWS input file
        self.nLayers = self.newModelParams.pop('nLayers', 2)
        self.backVisc = self.newModelParams.pop('backVisc', 1.e-4)  # the background viscosity (in m2/s).
        # Experiences suggest a value of 10-4 to 10-3 m2/s.

        self.alphaBreaking = self.newModelParams.pop('alphaBreaking', 0.6)  # threshold parameter at which to initiate
        # wave breaking
        self.betaBreaking = self.newModelParams.pop('betaBreaking', 0.3)  # threshold parameter at which to stop
        # wave breaking.
        self.dissipationBreaking = self.newModelParams.pop('dissipationBreaking', 0.25)  # (default = 1) This value
        # was 'used in Smits's paper 2014 CE
        self.turbModel = self.newModelParams.pop('turbModel', "KEPS")
        self.manningsN = self.newModelParams.pop('manningsN', 0.019)

        # length of sim time in [seconds]
        self.simulatedRunTime = self.newModelParams.pop('runDuration', 60 * 60)
        if self.simulatedRunTime > 3600:
            warnings.warn('The simulated RunTime is greater than 1 hour which could cause weird data processing '
                          'requests')

        # equilibration time in seconds for phase resolved model
        self.equlibTime = int(self.newModelParams.pop('equilbTime', 6 * 60))
        # convert to swash string and minutes
        self.equlibStr = self.convertTimeDeltatoSWASHString(DT.timedelta(minutes=self.equlibTime / 60))

        # start recording data at time in seconds
        self.startTimeSim = self.newModelParams.pop('startTimeSim', 0.0)
        self.startTimeSimStr = self.convertTimeDeltatoSWASHString(DT.timedelta(seconds=self.startTimeSim))

        # end time calculated [s]
        self.endTimeSim = self.startTimeSim + self.simulatedRunTime + self.equlibTime
        self.endTimeSimStr = self.convertTimeDeltatoSWASHString(DT.timedelta(seconds=self.endTimeSim))

        self.sampleRate = self.newModelParams.pop('sampleRate', 0.5)  # data output sample rate [s]
        self.timestep = self.newModelParams.pop('timeStep', 0.001)  # calculation timestep [s]

        print(f"still processing {self.newModelParams.keys()} from 'modelSettings' in input file")
        # if self.newModelParams.keys().any():
        #     raise TypeError('input params dictionary still has values in it')
        #

    def _check_input(self):
        """This function checks the ensure that the proper class items are set. It is used to check before writing
         input-files (could possibly be used for output as well)"""
        # assert self.WL is not None, "Need to set your waterLevel before writing file"
        assert self.fNameBase is not None, "please write _sws first, it sets outfile name base"
        assert self.workingDirectory is not None, "must set workingDirectory "
        assert self.equlibTime is not None, "Need to set equilibration Time before writing file"
        assert self.nLayers is not None, "Needed Value missing for writing files"

        assert self.backVisc is not None, "Needed Value missing for writing files"
        assert self.alphaBreaking is not None, "Needed Value missing for writing files"
        assert self.betaBreaking is not None, "Needed Value missing for writing files"
        assert self.dissipationBreaking is not None, "Needed Value missing for writing files"
        assert self.turbModel is not None, "Needed Value missing for writing files"
        assert self.manningsN is not None, "Needed Value missing for writing files"

        assert self.startTime is not None, "Needed Value missing for writing files"
        assert self.endTime is not None, "Needed Value missing for writing files"
        assert self.sampleRate is not None, "Needed Value missing for writing files"
        assert self.simulatedRunTime is not None, "Needed Value missing for writing files"
        assert self.equlibStr is not None, "Needed Value missing for writing files"
        assert self.endTimeSimStr is not None, "Needed Value missing for writing files"
        assert self.startTimeSimStr is not None, "Needed Value missing for writing files"
        assert self.timestep is not None, "Needed Value missing for writing files"

    def _preprocessCheck(self):
        """this function checks to make sure the path is in place and all files are in place needed to run a
        simulation. """
        print(" TODO: check to make sure all data are in place and in required input dictionaries ["
              "wrr.preprocessCheck]")
        # note: this will be defined by standardized dictionaries output from prepdata
        assert os.path.exists(self.workingDirectory), "working directory isn't in place properly"
        flist = ["{}.msh".format(self.fNameBase), 'spec.list', 'ww3_grid.nml', 'ww3_ounp.nml',
                 "{}.nc".format(self.fNameBase), 'namelists.nml', 'ww3_bounc.nml', 'ww3_ounf.nml']

    def _calculateSimulationCoreCount(self):
        """Calculates core count based on grid"""
        import multiprocessing as mp
        localCoreCount = mp.cpu_count()
        nCellPerCore = 500  # number of grid nodes per core
        self.simulationCoreCount = np.floor(self.nodeCount[0]).astype(int)
        if self.simulationCoreCount is None or self.simulationCoreCount > localCoreCount:
            self.simulationCoreCount = localCoreCount
            print("   Changed CPU count to {}".format(localCoreCount))

    def _generateRunStrings(self, modelExecutable):
        # preprocess string
        self.runString1 = f"mpiexec -n {self.simulationCoreCount} {modelExecutable} INPUT"

    def _postprocessCheck(self):
        print('Make sure all files are in the working Directory path')

    def _processSpatialData(self, fieldNC):
        # combine two dictionaries to one
        a = {**fieldNC[0], **fieldNC[1]}
        # round time to 1/100th of a second (resolve numerics)
        a['time'] = np.array([DT.datetime.fromtimestamp(p) for p in sb.baseRound([i.timestamp() for i in a['time']],
                                                                                 0.01)])
        return a

    def readAllFiles(self):
        """Reads all files from Swash model.  In this model it is a single mat file.

        Returns:
            field data and spatial data in dictionary formats.  Since there is no save point data,
            None is returned for the save point data.

        """
        if self.readFlag is True:
            self = pickle.load(open(self.pickleSaveName, 'rb'))
            # check output
            self._postprocessCheck()

            fieldNC = self.loadSwash_Mat(os.path.join(self.workingDirectory, self.fNameBase + '.mat'))

            # do we choose to output our data in a standard format?
            if self.rawOut is False:
                spatialData = self._processSpatialData(fieldNC)
                return spatialData, None

            else:
                return fieldNC, None

    def writeAllFiles(self, wavePacket, windPacket, wlPacket, bathyPacket, gridfname, **kwargs):
        """Take all files from preprocess and write the model input.

        Args:
            wavepacket: dictionary comes from prepspec
            windpacket: dictionary comes from prepwind
            WLpacket: dictionary comes from prepWaterLevel
            bathyPacket: dictionary comes from .prep_SwashBathy

        Keyword Args:
            savePoints: these are the save points for the model run [(lon,lat,'gaugeName1'),...]
        Returns:

        """
        if self.generateFiles is True:
            self._replaceDefaultParams()  # double check we're replacing the parameters appropriately
            self._check_input()  # check to make sure all data is in place before write
            del windPacket, gridfname

            print(f'writing all {self.modelName} input files')
            self.write_sws(bathyPacket, wlPacket)
            self.write_spec1D(wavePacket['freqbins'], wavePacket['fspec'])
            self.write_bot(bathyPacket['elevation'])

            # calculate number of cores to run simulation
            self._calculateSimulationCoreCount()

    def runSimulation(self, modelExecutable):
        """ generates input and checks all files are in place, then runs simulation

        Args:
            modelExecutable: full path of model model executable

        Returns:
            None

        """
        if self.runFlag is True:
            # generate appropriate run strings
            self._generateRunStrings(modelExecutable)
            # check appropriate data are in place
            self._preprocessCheck()

            # switch to directory and run
            os.chdir(self.workingDirectory)  # changing locations to where input files should be made

            # run prepossessing scripts and simulation
            dt = DT.datetime.now()
            print('Running {} Simulation starting at {}'.format(self.modelName, dt))
            _ = check_output(self.runString1, shell=True)
            self.simulationWallTime = DT.datetime.now() - dt
            print('Simulation took {:.1f} minutes'.format(self.simulationWallTime.total_seconds() / 60))
            os.chdir(self.cmtbRootDir)

            # Now re-save metadata pickle, with appropriate simulation simulatedRunTime data
            with open(self.pickleSaveName, 'wb') as fid:
                pickle.dump(self, fid, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            print('I might be doing something wrong by loading and re-assigning self!!!!')
            with open(self.pickleSaveName, 'rb') as fid:
                self = pickle.load(fid)

    # write functions

    def convertTimeDeltatoSWASHString(self, timeDeltaObj):
        """Function checks/converts time delta objects to swash format (in string)."""
        hours = timeDeltaObj.total_seconds() // 3600
        minutes = (timeDeltaObj.total_seconds() % 3600) // 60
        seconds = (timeDeltaObj.total_seconds() % 60)
        return "{:02}{:02}{:02}.000".format(int(hours), int(minutes), int(seconds))

    def write_sws(self, gridDict, WLpacket):
        """ This function writes Regular Grid input file for the SWASH model
        This function pulls Water level from the initalized class
        WRITE THIS FUNCTION FIRST

        Args:
            fNameBase(str): this function assumes all of the boundary, grid, files have the same name with
                a different file extension.  Convention is to use a datestring for the time of the model run
                (eg: YYYYmmhhTHHMMSSZ iso standard time, without ':'s )
            WLvalue (float): waterlevel value (model setup assumes NAVD88, but must be same datum as bot file)
            gridDict (dictionary): grid information
                'mx'
                'my'
                'dx'
                'dy'
                'xpc'
                'ypc'
                'alpc'

        Returns:
            None

        """
        projectName = 'VerPrefix: {}'.format(self.versionPrefix)  # meta data
        metaField2 = '_'  # meta data
        dataReturnString = 'XP YP BOTL WATL VEL VELK USTAR NHPRSK VZ'
        # note: my string notation is done with double so single quotes can be written into SWASH input file
        ##################### set variables for file write -- variable
        mx = gridDict['mx']  # number of bathy grid outputs
        my = gridDict['my']  # number of bathy grid outputs
        dx = int(gridDict['dx'])  # mesh/grid resolution [m]
        dy = int(gridDict['dy'])  # mesh/grid resolution [m]
        self.WL = WLpacket['avgWL'].squeeze()
        assert np.size(self.WL) == 1, "WL needs to be of value 1"

        ##########################
        modelStationarity = "NONSTationary"
        ModelMode = "TWODimensional"
        gridType = 'REGular'
        ##########################
        # settings  for reading grd file  -- these might change with FRF coordinate system
        ## see page 40/41 - chapter 4 of SWAN manual for  more information (SWASH and SWAN are similar)
        grdFac = 1  # multiplication factor for all values read from file (eg 1, -1, or 0.1 for
        # decimeter conversion to [m])
        idla = 1  # prescribes the order in which the values of bottom levels and other fields
        # should be given in file [1, 2, 3, 4 or 5]
        nhedf = 0  # number of header lines at start of file
        nhedvec = 0  # number of header lines in the file at the start of each component
        fortranFormat = 'FREE'  # fortran format [FREE or FORMAT]
        ###########################
        # physical parameters settings
        nLayers = self.nLayers

        backVisc = self.backVisc  # the background viscosity (in m2/s). Experiences suggest a value of 10-4 to 10-3
        alphaBreaking = self.alphaBreaking  # threshold parameter at which to initiate wave breaking
        betaBreaking = self.betaBreaking  # threshold parameter at which to stop wave breaking.
        dissipationBreaking = self.dissipationBreaking  # (default = 1) This value was used in Pieter's paper 2014 CE
        turbModel = self.turbModel
        manningsN = self.manningsN

        startTime = self.startTimeSim  # start time in seconds
        sampleRate = self.sampleRate  # sample rate in seconds
        RunTime = self.simulatedRunTime  # length of simulated time (or collection) in [seconds]
        endTime = self.endTimeSim
        equlibStr = self.equlibStr
        endTimeStr = self.endTimeSimStr
        startTimeStr = self.startTimeSimStr
        timestep = self.timestep

        ####################################
        if nLayers > 6:
            warnings.warn('Check Friction, Breaking, and Numerics, these were not previously set@@@@!!! ')
        # file names for output and read
        grdFile = '{}.grd'.format(self.fNameBase)  # grid data
        self.ofname_sws = 'INPUT'  # file we are writing out called
        botFname = '{}.bot'.format(self.fNameBase)  # bathy elevations
        offshoreBoundaryFile = '{}.bnd'.format(self.fNameBase)  # the name of the offshore boundary
        outputMatFile = '{}.mat'.format(self.fNameBase)  # what's model output
        print(' TODO: calculate equlib time based on conditions [wrr.writeSWS]')
        ########################## set variables for file write -- static
        assert gridType in ["REGular", "CURVilinear"], "Check Grid type"  # list of grid Types available
        ##########################
        # bathymetry settings INPGRID BOTTOM
        bottomFac = -1  # multiplaction factor for all values read from file (eg 1, -1, or 0.1 for
        # decimeter conversion to [m])
        mxinp = int(mx - 1)
        myinp = int(my - 1)  # number of mesh
        dxinp = int(dx)  # bathy grid dx
        dyinp = int(dy)  # bathy grid dy
        xpinp = 0  # origin in FRF coord
        ypinp = round(gridDict['ypc'])  # origin in FRF coord
        alpinp = 0  # rotation
        ###########################
        # regular grid computational Settings
        gridType = 'REGULAR'
        # computational grid stuff
        xpc = 0  ## set at zero for simplicity  # origin of computational grid in larger coord
        ypc = round(gridDict['ypc'])  # origin of computational grid in larger coord
        alpc = round(gridDict['alpc'])  # degrees counter clockwise rotation from true North
        xlenc = int(mxinp * dx)  # length of the computational grid in x -direction (in m).
        ylenc = int(myinp * dy)  # length of the computational grid in y -direction (in m)
        mxc = int(mxinp)  # number of meshes in computational grid in x -direction for a uniform
        myc = int(myinp)  # number of meshes in computational grid in y -direction for a uniform
        ### model output and compute request stuff
        outputLocationOnshore = int(ylenc / 2)
        outputLocationOffshore = int(ylenc / 2)
        ###################### write file now ################################################
        nowString = DT.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        f = open(os.path.join(self.workingDirectory, self.ofname_sws), 'w')
        f.write(
            "$*************HEADING***********************************\n$ Coastal Model Test Bed SWASH setup up.\n$\n$\n")
        f.write("$ file written at: {}\n".format(nowString))
        # f.write("$ wave Hs = {:.2f}; wave Tp = {:.2f}s;\n$wave Dm = {:.2f}; wave Dir Spread {}\n".format(self.Hs,
        #                                                                                                  self.Tp,
        #                                                                                                  self.Dm,
        #                                                                                                  self.spreadD))
        f.write("$ if the above are 'None', then the IO\n$ class wasn't properly initiated\n")
        f.write("PROJ '{}' '{}'\n".format(projectName[:16], metaField2))  # 16 char limit
        f.write("$\n$ This file is automatically Generated as part of CMTB\n" +
                "$ written by: Spicer Bak, with help from Julia Fieldler\n")
        f.write("$***********MODEL INPUT*********************************\n$\n")
        f.write("MODE {} {}\n".format(modelStationarity, ModelMode))
        f.write("$\n$\n$Grid Descriptors \n$\n")
        if gridType == 'REGULAR':
            #                                                [xpc] [ypc] [alpc] [xlenc] [ylenc] [mxc] [myc]
            f.write('CGRID {} {:.2f} {:.2f} {} {:6d} {:6d} {:6d} {:6d}\n'.format(gridType, xpc, ypc, alpc,
                                                                                 xlenc, ylenc, mxc, myc))
        else:
            raise NotImplementedError('Only grid currently setup is Regular')
        f.write("$\n$\n$\n$Grid coordinates file\n$\n")
        #         f.write("READinp COORdinates {} {} {} {} {} {}\n$\n".format(grdFac, grdFile,
        #         idla, nhedf, nhedvec, fortranFormat))
        #                                                [xpinp] [ypinp][alpinp][mxinp][myinp][dxinp][dyinp]
        f.write("$\nINPGRID BOTTOM {} {:.2f} {:.2f} {} {} {} {:d} {:d}\n$\n".format(gridType, xpinp, ypinp, alpinp,
                                                                                    mxinp, myinp, dxinp, dyinp))
        f.write("$\n$Vertical Layers\n$\n")
        f.write("VERT {}\n".format(nLayers))
        f.write("$\n$\n$Bathymetry values (*.bot file)\n$\n")
        f.write("READINP BOTTOM {} '{}' {} {} {}\n".format(bottomFac, botFname, idla, nhedf, fortranFormat))
        f.write("$\n$\n$Set Water Level values\n$\n")
        f.write("SET level = {}\n".format(self.WL.squeeze()))
        f.write("$\n$\n$Set Friction, Viscosity, Breaker, etc\n$\n")
        f.write("FRIC MANN {}\n".format(manningsN))
        f.write("SET BACKVISC {}\n".format(backVisc))
        f.write("BREAK {} {} {}\n".format(alphaBreaking, betaBreaking, dissipationBreaking))
        f.write("VISC VERT {}\n".format(turbModel))
        f.write("$\n$Set Spectral Boundary\n$\n")
        f.write("BOUN SIDE EAST BTYPE WEAK CON SPECfile '{}'\n".format(offshoreBoundaryFile))
        ##### NUMERICS -- HARD CODED! #####
        f.write("$\n$Set Numerics (these are hardcoded for now)\n$\n")
        f.write("$\nNONHYDROSTATIC BOX 1 PRECONDITIONER ILU\nDISCRET CORRDEP MUSCL\n")
        f.write("DISCRET UPW UMOM MOM VERT FIR\nDISCRET UPW UMOM MOM HOR MUSCL\nTIMEI 0.05 0.2\n")
        f.write("$***********MODEL OUTPUT REQUESTS*********************************\n$\n")
        f.write("GROUP 'LINE' {} {:d} {} {}\n".format(1, int(mxc), int(outputLocationOnshore), outputLocationOffshore))
        # define which output we want
        f.write("BLOCK 'LINE' NOHEAD '{}' LAY 1 {} OUTPUT  {} {} SEC\n".format(outputMatFile, dataReturnString,
                                                                               equlibStr, sampleRate))
        f.write("TEST 1 0\n")  # write out time series to print file (aka log file)
        f.write("COMPUTE {} {} SEC {}\nSTOP".format(startTimeStr, timestep, endTimeStr))
        f.close()

    def write_bnd(self, freqbins, dirbins, spec, loc):
        """write spectral boundary conditions, requires a preprocessing step for determining
        the df (and other things)
        Arguments:
            ofname(str): File name for output
            freqbins(array): Vector of frequency spacing of the two-dimensional spectrum
            dirbins(array): Vector of directional spacing of the two-dimensional spectrum
            spec(array): Frequency-directional spectrum (expected units is m^2/Hz/Deg). Also it
                         is assumed that the spectrum is a 2-dimensional variable with a structure
                         Spec(NFREQ,NDIR). NFREQ is the number of frequencies and NDIR is the
                         number of directions
            Loc(array): Co-ordinates for location at which boundary information is provided (i.e., Loc = [Lon,Lat])


        # this was converted from a matlab script originally for SWAN generated by:
        % Nirnimesh Kumar and George Voulgaris
        % Coastal Processes and Sediment Dynamics Lab
        % Dept. of Earth and Ocean Sciences,
        % Univ. of South Carolina, Columbia, SC
        % 03/06/2013
        % Adapted by Julia Fiedler and Nirnimesh Kumar 9/9/2014 for 1D spectrum
        % Adapted by Julia Fiedler for use in SWASH model 10/24/2016 with PUV
        % spectra
        ## adapted for python by Spicer Bak
        """
        offshoreBoundaryFile = os.path.join(self.workingDirectory, self.fNameBase + '.bnd')

        NLOC = 1  # Number of locations
        NFREQ = len(freqbins)  # Number of frequencies
        NDIR = len(dirbins)  # Number of directions
        rho = 1025  # SWAN allows changing rho value, but deafult is 1025 kg/m^3
        g = 9.81  # Accn. due to gravity
        ver = 'N/A'  # SWAN version
        proj = 'CMTB'  # Project Name
        Exval = -999  # Exception value
        # write file header
        f = open(offshoreBoundaryFile, 'w');
        f.write('SWASH   1                                SWASH standard spectral file, version\n');
        f.write('   Data produced by SWASH version {} \n'.format(ver))
        f.write('$   Project: {}\n'.format(proj))
        f.write('LOCATIONS                                  locations in x-y space\n')
        f.write('{}                                  number of locations'.format(NLOC))
        for loc in loc:
            f.write('%12.6f %12.6f\n'.format(loc[0], loc[1]))
        f.write('AFREQ                                   absolute frequencies in Hz\n');
        f.write('{}'.format(NFREQ));
        f.write('                                  number of frequencies\n');
        for freq in freqbins:
            f.write('{}\n'.format(freq));

        f.write('NDIR                                    spectral nautical directions in degr\n');
        f.write('{}'.format(NDIR))
        f.write('                                  number of directions\n');
        for waveDir in dirbins:
            f.write('{}\n'.format(waveDir))
        f.write('QUANT\n');
        f.write('     1                                  number of quantities in table\n');
        f.write('VaDens                                  variance densities in m2/Hz/degr\n');
        f.write('m2/Hz/degr                             unit\n');
        f.write('{}                          exception value\n'.format(Exval))

        for q in range(NLOC):
            Edens = np.squeeze(spec[q, :, :]);  # isolate single spectra
            ID = np.max(np.max(Edens))  # spectral max
            # normalize spectra so the smallest value is 1
            if ID > (10 ** (-10)):
                FAC = (1.01 * ID * 10 ** (-4))
            else:
                FAC = 10 ** (-5)

            Edens = Edens / FAC  # normalize spectra so no decimals
            # [[fill]align][sign][#][0][minimumwidth][.precision][type] # pep 3101
            f.write('FACTOR\n')
            f.write("{: >13.8E}\n".format(FAC))
            for r in range(NFREQ):
                f.write('{: 6d}\n'.format(np.round(Edens[r, :])))
        f.close()

    def write_grd(self, xCoord, yCoord):
        """write out a SWASH grd file

        Args:
            xCoord (array): array of X coordinates of mesh points
            yCoord (array): array of Y coordinates of mesh points


        """
        fname = os.path.join(self.workingDirectory, self.fNameBase + '.bot')
        # Print the grid coordinates to the grid file
        f = open(fname, 'w')
        f.write('{:12.6f}\n'.format(xCoord))
        f.write('{:12.6f}\n'.format(yCoord))
        f.close()

    def write_bot(self, h):
        """write bottom elevation file

        Arguments:
            h(array): array of bottom elevations 2D

        """
        self.nodeCount = np.shape(h)
        xx, yy = np.shape(h)
        fname = os.path.join(self.workingDirectory, self.fNameBase + '.bot')
        f = open(fname, 'w');
        for idxX in range(xx):
            for idxY in range(yy):
                f.write('   {:.2f}'.format(h[idxX, idxY]))
            f.write('\n')
        f.write('\n')
        f.close()

    def write_spec1D(self, freqbins, energy):
        """write spectral boundary condition for 1D spectra

        Args:
            freqbins(array): frequency bins for spectra
            energy(array): associated energy at each frequency [m^2/hz]

        Returns:
            None

        """
        fname = os.path.join(self.workingDirectory, '{}.bnd'.format(self.fNameBase))
        f = open(fname, 'w')
        f.write('SPEC1D\n')
        # f.write('BOUN SIDE EAST BTYPE WEAK CON\n')  # tell the model how to read file
        for i in range(len(freqbins)):
            f.write('{:10.4E} {:10.4E}\n'.format(freqbins[i], energy[i]))
        f.close()

    # Now Read functions

    def loadSwash_Mat(self, fname):
        """This function will load the model output file, it will pull the input water level from the
        preinitalized instance
        # file: Filename of  matlab file as generated  by  SWASH.

        Args:
            fname (str): the input file name to load

        Returns:
            Data dictionary with keys directly associated from matfile output
                'time': UTC time stamp of simulation data (after equilib time removed)
                'elevation': bottom elevation for simulation NAVD88
                'xFRF': data['Xp'].squeeze(),
                'yFRF': data['Yp'].squeeze(),
                'eta':  surface position in NAVD88
                'Ustar': magnitude of friction velocity
                'velocityU': cross-shore surface velocity
                'velocityV': surface alongshore velocities
                'velocityUprofile': cross-shore velocity profiles    [time, yFRF, xFRF, z]
                'velocityVprofile': profile of alongshore velocities [time, yFRF, xFRF, z]
                'velocityZprofile': profile of z velocities          [time, yFRF, xFRF, z]
                'NormPresProfile': profile of normalized non hydrostatic pressure

            metaDict with below keys
                'waveDm': mean direction at boundary
                'waveHs': significant wave height at boundary
                'waveTp': wave peak period at boundary
                'WL': water level used ,
                'nLayers': number of layers in model
                'nprocess': number of compute processes
                'equlibTime': equilibration time used before writing data to file
                'simWallTime': wall time it took to run simulation
                'spreadD': directional spread at boundary
                'versionPrefix': verison prefix of simulation

        """
        from scipy import io

        assert fname[-3:] == 'mat', 'expected output file is a matfile'
        # assert self.WL is not None, 'Needs self.WL before loading files'
        # --------------------------------------------------------------------------
        # Check how long it takes to load data
        import time
        start = time.time()
        # if the file exists, then import and parse it
        if not os.path.exists(fname):
            raise IOError('SWASH:  no simulation output file present\n{}'.format(fname))

        data = io.loadmat(fname)
        dataOUT, dataTemp, runMeta = {}, {}, {}
        # initalize outDict with empty arrays
        times, nonTimeDependant = [], []
        # first load all vars and parse as time dependent array
        for dictInKey, dataValues in data.items():  ## should i sort these?
            origVarName = dictInKey.split('_')
            saveKey = ''.join(origVarName[:-2])
            # print('Looking through var {} will save as {} or {}'.format(origVarName, saveKey, dictInKey))
            try:
                timeString = origVarName[-2] + '_' + origVarName[-1]
                try:
                    d = DT.datetime.strptime(timeString, "%H%M%S_%f")
                    times.append(
                        DT.timedelta(hours=d.hour, minutes=d.minute, seconds=d.second, microseconds=d.microsecond))
                    # print('saved as time step {}'.format(timeString))
                except ValueError:  # this will be things like __header__, __global__... etc, errors out on d = ...
                    runMeta[origVarName[2]] = dataValues
                    continue

                ######## now write data to temp dictionary
                # save data as 1D arrays, to reshape later
                # print('Original key {} put {} values into key {}'.format(origVarName, dataValues.shape, saveKey))
                if saveKey not in dataTemp:  # then haven't parsed it before, just add it
                    dataTemp[saveKey] = [dataValues]
                else:  # just add the data !
                    dataTemp[saveKey].append(dataValues)

            except IndexError:  # for not time dependant variables
                # print('Original key {} put {} values into key {}'.format(origVarName, dataValues.shape, dictInKey))
                # just save them as is  (variables like Xp, because save key turns into gibberish)
                nonTimeDependant.append(dictInKey)
                dataTemp[dictInKey] = [dataValues]
                # pass

        ################### reshape list structure to 3 d array
        # parsed quickly to a single dictionary, now reshape to [t, y, x]
        # assume that we're always outputing eta and use this to get number of timesteps
        # turn nan's to masks for output
        # tSteps, nY, nX = np.shape(dataTemp['Watlev'])
        t = DT.datetime.now()
        for var in dataTemp.keys():
            if var not in nonTimeDependant:
                dataOUT[var] = np.ma.MaskedArray(dataTemp[var], mask=np.isnan(dataTemp[var]))
        ##############################################################################
        # now restructure dictionary with a bunch of keys to a single
        # dictionary with multi dimensional output (concatenate the layered values)
        ##############################################################################
        for var in list(dataOUT.keys()):
            # if var in meshVars: # then variables have same number as layers
            saveKey = var.translate(var.maketrans('', '', '0123456789'))
            if saveKey != var:  # then there's not associated with it
                if saveKey in dataOUT:
                    dataOUT[saveKey] = np.append(dataOUT[saveKey], np.expand_dims(dataOUT[var], axis=-1), axis=-1)
                else:
                    dataOUT[saveKey] = np.expand_dims(dataOUT[var], axis=-1)
                del dataOUT[var]

        d1 = DT.datetime.strptime(self.fNameBase, self.dateStringFmt)
        # wrap up into output dictionary named data
        dataDict = {'time': d1 + np.unique(times),  # convert each time step to date time from time delta object
                    'elevation': data['Botlev'].squeeze(),
                    'xFRF': data['Xp'].squeeze(),
                    'yFRF': data['Yp'].squeeze(),
                    'eta': dataOUT['Watlev'],
                    'Ustar': dataOUT['Ustar'],
                    'velocityU': dataOUT['velx'],
                    'velocityUprofile': dataOUT['velkx'],
                    'velocityV': dataOUT['vely'],
                    'velocityVprofile': dataOUT['velky'],
                    'velocityZprofile': dataOUT['w'],
                    'NormPresProfile': dataOUT['Nprsk'], }

        metaDict = {  # 'waveDm': self.Dm,
            # 'waveHs': self.Hs,
            # 'waveTp': self.Tp,
            # 'WL': self.WL,
            'nLayers': self.nLayers,
            'nprocess': self.simulationCoreCount,
            'equlibTime': self.equlibTime,
            'simWallTime': self.simulationWallTime,
            # 'spreadD': self.spreadD,
            'versionPrefix': self.versionPrefix}

        print(' loading SWASH data takes: {:.2f} seconds'.format(time.time() - start))
        return dataDict, metaDict