'''
Created on Aug 20, 2011

@author: Piotr
'''
from generator.data.GeneratorDescription import GeneratorDescription

import os
from generator.scene.SceneInjecterX3D import SceneInjecterX3D

class RunnerBase(object):
    '''
        Abstract base class for runner
    '''
    def execute(self):
        raise NotImplementedError("This is abstract method")

class BlenderRunner(RunnerBase):
    '''
        Class uses the injected scene generator and @see: GeneratorDescription objects
    '''

    def __init__(self, generatorDescription, sceneGenerator, renderGenerator, rootFolder):
        '''
        Constructor
        @param generatorDescription: object of class @see: GeneratorDescription
        @param sceneGenerator: implementation of the @see: SceneGeneratorBase
        @param renderGenerator: implementation of the @see: RenderGeneratorBase
        '''
        self.generatorDescription = generatorDescription
        self.sceneGenerator = sceneGenerator
        self.renderGenerator = renderGenerator

        # TODO: passed via constructor
        self.sceneInjecter = SceneInjecterX3D()

        # TODO: passed via constructor
        self.rootFolder = rootFolder

        self._base_command = "blender -b --python "

        # read the file with data model (x3d) and make it DEFAULT !
        model_data_file = self.generatorDescription.getInputFilePath()
        with open(model_data_file, mode='r') as file :
            self.render_text = " ".join(file.readlines())


    def __buildCommand(self, inputScript):
        '''
            Concatenates the command
        '''
        return self._base_command + inputScript


    def __tryCreatingFolder(self, folder):
        '''
            Creates new folder if there is no such foldeer 
            if there is then raises exception 
        '''
        print("Making folder: " + folder)
        if not os.path.isdir(folder):
            os.mkdir(folder)
        else :
            path = os.path.abspath(folder)
            raise RuntimeError("The specified folder already exists: " + path)

    def __createOutputFolders(self):
        '''
            Creates the output folders
            For default version this are:
                - models/
                - renders/
                - scripts/
            under the root blender_run_{date} || so called root folder
        '''
        self.__tryCreatingFolder(self.rootFolder)

        modelsPath = os.path.join(self.rootFolder, self.generatorDescription.inputFolder)
        rendersPath = os.path.join(self.rootFolder, self.generatorDescription.outputFolder)
        scriptsPath = os.path.join(self.rootFolder, "scripts")

        self.__tryCreatingFolder(modelsPath)
        self.__tryCreatingFolder(rendersPath)
        self.__tryCreatingFolder(scriptsPath)

    def __createModelFile(self, scene, counter):
        '''
            Uses the render script to do the proper file handling
        '''
        # some basics
        inputFormat = self.generatorDescription.inputFormat

        # create model name and final name for this iteration
        final_name = self.__getFormattedName(counter) + inputFormat;

        # get absolute path locations of the elements
        path = os.path.join(self.rootFolder, self.generatorDescription.inputFolder)
        model_final = os.path.join(path, final_name)
        model_final = os.path.abspath(model_final)

        print("Model final")
        print(model_final)

        # use injector to put values into the file stream
        output = self.sceneInjecter.injectScene(self.render_text, scene)

        # saving file into the provided inputFileName
        with open(model_final, mode="w") as file:
            file.write(output)

        return model_final

    def __getFormattedName(self, counter):
        inputFileName = self.generatorDescription.inputFileName
        return inputFileName + "_" + str(counter)

    def __createRenderFile(self, counter):
        '''
            Creates the render file in the scripts folder
        '''

        # generate render.py with corresponding final name         
        render_script_file = self.__getFormattedName(counter) + ".py"

        path = os.path.join(self.rootFolder, "scripts")
        render_script_file = os.path.join(path, render_script_file)
        render_script_file = os.path.abspath(render_script_file)


        final_name = self.__getFormattedName(counter)

        render_script = self.renderGenerator.prepareRender(final_name)

        print("Render file")
        print(render_script_file)

        # save the render script into proper folder
        with open(render_script_file, mode="w") as file:
            file.write(render_script)

        return render_script_file

    def execute(self):
        '''
            Runs the script and returns the string with output.
            Logs the output.
        '''
        # create the output folders
        self.__createOutputFolders()

        # get all the renderings
        scenes = self.sceneGenerator.prepareScenes()
        i = 0
        for scene in scenes:
            model_file = self.__createModelFile(scene, i)

            render_file = self.__createRenderFile(i)

            # get the rendering
            command = self.__buildCommand(render_file)

            print(command)

            #TODO: make it loggable
            stream = os.popen(command)
            print(stream.read())

            i += 1
