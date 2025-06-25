import os

import numpy as np
import pygame
from OpenGL.GL import *

from hitbox import Hitbox


class OBJ:
    generate_on_init = True

    @classmethod
    def loadTexture(cls, imagefile):
        surf = pygame.image.load(imagefile)
        image = pygame.image.tostring(surf, 'RGBA', 1)
        ix, iy = surf.get_rect().size
        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        return texid

    @classmethod
    def loadMaterial(cls, filename):
        contents = {}
        mtl = None
        dirname = os.path.dirname(filename)

        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'newmtl':
                mtl = contents[values[1]] = {}
            elif mtl is None:
                raise ValueError("mtl file doesn't start with newmtl stmt")
            elif values[0] == 'map_Kd':
                # load the texture referred to by this declaration
                mtl[values[0]] = values[1]
                imagefile = os.path.join(dirname, mtl['map_Kd'])
                mtl['texture_Kd'] = cls.loadTexture(imagefile)
            else:
                try:
                    mtl[values[0]] = list(map(float, values[1:]))
                except ValueError:
                    mtl[values[0]] = values[1:]
        return contents

    def __init__(self, filename, position=np.zeros(3), rotation=np.zeros(3), scale=np.ones(3),
                 hitbox_size=np.array([1.0, 1.0, 1.0]), swapyz=False):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.gl_list = 0
        dirname = os.path.dirname(filename)
        self.hitbox = Hitbox(position, hitbox_size)

        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append(list(map(float, values[1:3])))
            elif values[0] in ('usemtl', 'usemat'):
                if len(values) < 2:
                    material = "Material"
                else:
                    material = values[1]
            elif values[0] == 'mtllib':
                self.mtl = self.loadMaterial(os.path.join(dirname, values[1]))
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))
        if self.generate_on_init:
            self.generate()

        self.position = position
        self.rotation = rotation
        self.scale = scale

    def generate(self):
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)

        glEnable(GL_TEXTURE_2D)  # <— enable once
        glFrontFace(GL_CCW)

        for face in self.faces:
            vertices, normals, texcoords, material = face
            mtl = self.mtl[material]

            # Make sure we draw textured faces in white, so the texture shows
            glColor3f(1.0, 1.0, 1.0)

            if 'texture_Kd' in mtl:
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                # “Unbind” any texture, fall back to flat color
                glBindTexture(GL_TEXTURE_2D, 0)
                glColor3fv(mtl['Kd'])

            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texcoords[i] > 0:
                    glTexCoord2fv(self.texcoords[texcoords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()

        glDisable(GL_TEXTURE_2D)
        glEndList()

    def render(self):
        glPushMatrix()  # Save the current transformation state
        # Nutze die aktuelle Position (z.B. für Animationen)
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(self.rotation[0], 1, 0, 0)  # Rotate around X-axis
        glRotatef(self.rotation[1], 0, 1, 0)  # Rotate around Y-axis
        glRotatef(self.rotation[2], 0, 0, 1)  # Rotate around Z-axis
        glScalef(*self.scale)
        glCallList(self.gl_list)
        glPopMatrix()  # Restore the previous transformation state

    def free(self):
        glDeleteLists([self.gl_list])
